#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DUMP_DIR="$PROJECT_DIR/dump"

if docker compose version >/dev/null 2>&1; then
	DC=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
	DC=(docker-compose)
else
	echo "Error: neither 'docker compose' nor 'docker-compose' is available."
	exit 1
fi

IN_FILE="${1:-}"

if [[ -z "$IN_FILE" ]]; then
	IN_FILE="$(ls -1t "$DUMP_DIR"/odoo_backup_*.dump 2>/dev/null | head -n 1 || true)"
	if [[ -z "$IN_FILE" ]]; then
		echo "No backup provided and no dump found in $DUMP_DIR"
		exit 1
	fi
fi

if [[ ! -f "$IN_FILE" ]]; then
	echo "File not found: $IN_FILE"
	exit 1
fi

FS_FILE="${IN_FILE%.dump}_filestore.tar.gz"

cd "$PROJECT_DIR"
trap 'rc=$?; if [[ $rc -ne 0 ]]; then echo "Import failed. web is left stopped; the database may be incomplete."; fi' EXIT

echo "Stopping web container..."
"${DC[@]}" stop web

echo "Starting db container..."
"${DC[@]}" up -d --wait db

echo "Recreating database..."
"${DC[@]}" exec -T db sh -c 'dropdb -U "$POSTGRES_USER" --if-exists "$ODOO_DB_NAME" && createdb -U "$POSTGRES_USER" "$ODOO_DB_NAME"'

echo "Restoring database from: $IN_FILE"
"${DC[@]}" exec -T db sh -c 'pg_restore -U "$POSTGRES_USER" -d "$ODOO_DB_NAME" --no-owner --exit-on-error' < "$IN_FILE"

MODULES="$("${DC[@]}" exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$ODOO_DB_NAME" -tAc "select count(*) from ir_module_module"' | tr -d '[:space:]')"
if [[ -z "$MODULES" || "$MODULES" -le 0 ]]; then
	echo "Error: restored database has no Odoo modules."
	exit 1
fi

if [[ -f "$FS_FILE" ]]; then
	echo "Restoring filestore from: $FS_FILE"
	"${DC[@]}" run --rm --no-deps -T --entrypoint sh web -c 'rm -rf /var/lib/odoo/* && tar xzf - -C /var/lib/odoo' < "$FS_FILE"
else
	echo "Warning: No filestore backup found at $FS_FILE, skipping."
fi

echo "Starting full stack..."
"${DC[@]}" up -d

echo "Done. Database imported."
