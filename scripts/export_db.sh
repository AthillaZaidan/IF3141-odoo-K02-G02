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

cd "$PROJECT_DIR"
mkdir -p "$DUMP_DIR"

TS=$(date +%Y%m%d_%H%M%S)
DB_FILE="${1:-$DUMP_DIR/odoo_backup_${TS}.dump}"
FS_FILE="${DB_FILE%.dump}_filestore.tar.gz"

# Remove partial output if anything below fails
trap 'rc=$?; if [[ $rc -ne 0 ]]; then rm -f "$DB_FILE" "$FS_FILE"; echo "Export failed."; fi' EXIT

echo "Starting db container..."
"${DC[@]}" up -d --wait db

echo "Exporting database to: $DB_FILE"
"${DC[@]}" exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$ODOO_DB_NAME" -Fc' > "$DB_FILE"
if [[ ! -s "$DB_FILE" ]]; then
	echo "Error: database dump is empty."
	exit 1
fi

# Reuses the web image and its volume mapping; --no-deps keeps web from starting
echo "Exporting filestore to: $FS_FILE"
"${DC[@]}" run --rm --no-deps -T --entrypoint tar web czf - -C /var/lib/odoo . > "$FS_FILE"
if [[ ! -s "$FS_FILE" ]]; then
	echo "Error: filestore archive is empty."
	exit 1
fi

echo "Done. Backup files:"
echo "  DB:        $DB_FILE"
echo "  Filestore: $FS_FILE"
