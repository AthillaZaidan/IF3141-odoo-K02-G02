# IF3141 Sistem Informasi — Template Odoo

Template tugas besar IF3141: Odoo 17 + PostgreSQL 16 lewat Docker. Yang Anda buat adalah **modul (addon)** Odoo, bukan plugin. Contoh modul yang benar ada di `custom_addons/starter_cats`.

Klik **Use this template** di GitHub untuk membuat repository (private) milik kelompok.

## Prasyarat

- Docker (Docker Desktop di Windows/Mac) dan Git
- Python 3.11 — opsional, hanya untuk lint/IDE (bukan untuk menjalankan Odoo)

## Mulai cepat

```bash
cp .env.example .env        # Windows: copy .env.example .env
# ubah POSTGRES_PASSWORD di .env
docker compose up -d
```

Buka http://localhost:8069. Pada start pertama Odoo membuat database `odoo_app` (nama dari `ODOO_DB_NAME`); tunggu beberapa saat sampai halaman login muncul. Login awal: `admin` / `admin`. **Ganti password admin** setelah login.

## Perintah harian

| Keperluan | Perintah |
|---|---|
| Mulai | `docker compose up -d` |
| Lihat log | `docker compose logs -f web` |
| Berhenti (data tetap) | `docker compose down` |
| Berhenti dan **MENGHAPUS data** | `docker compose down -v` |
| Setelah mengubah Python | `docker compose restart web` |
| Install modul | `docker compose run --rm web odoo -d odoo_app -i starter_cats --stop-after-init` |
| Upgrade modul | `docker compose run --rm web odoo -d odoo_app -u starter_cats --stop-after-init` |
| Test modul | `docker compose run --rm web odoo -d odoo_test -i starter_cats --test-enable --test-tags /starter_cats --stop-after-init --without-demo=all` |
| Backup database | `./scripts/export_db.sh` (Windows: `scripts\export_db.cmd`) |
| Restore database | `./scripts/import_db.sh` (Windows: `scripts\import_db.cmd`) |

Catatan:

- Gunakan `docker compose run --rm web odoo ...`, bukan `exec`: hanya `run` melewati entrypoint yang memasang koneksi database dari `.env`.
- Perubahan file XML dan Python dimuat ulang otomatis (`--dev=reload,xml`); perubahan model (field baru) tetap perlu **Upgrade modul**.
- Menjalankan test untuk kedua kalinya pada `odoo_test` yang sama: ganti `-i` dengan `-u`.
- Backup menyimpan dump database dan filestore ke `dump/` (tidak di-commit). Restore **menimpa** database `ODOO_DB_NAME`; jika restore gagal, skrip berhenti dengan kode error dan `web` dibiarkan mati. Dump harus dipulihkan ke nama database yang sama dengan saat di-export, karena filestore Odoo disimpan per nama database.

## Struktur folder

| Path | Isi |
|---|---|
| `custom_addons/` | Modul Anda (di-mount ke `/mnt/extras-addons`) |
| `config/odoo.conf` | Konfigurasi Odoo untuk development |
| `config/odoo.prod.conf.example` | Contoh konfigurasi deployment (tidak dipakai compose) |
| `dump/` | Hasil backup (di-ignore git) |
| `scripts/` | Skrip backup/restore (`.sh` dan `.cmd`) |
| `docs/` | Daftar bab guide |
| `DATA.md` | Pemetaan data pribadi untuk sistem Anda |
| `.env.example` | Contoh variabel lingkungan; salin ke `.env` |

## Modul starter: `starter_cats`

Contoh modul (domain kucing) berisi model dengan chatter, state machine dengan guard, constraint, group + ACL + record rule, view `<tree>`/form/search, data awal (`noupdate`), data demo, dan test. Pasang dengan perintah **Install modul** di atas; bila modul belum muncul di **Apps**, pilih **Update Apps List**.

## IDE dan lint

Salin source Odoo agar editor bisa autocomplete (hanya file yang dibutuhkan, ±70 MB; folder di-ignore git):

```bash
mkdir .odoo-src
docker compose run --rm -T --no-deps --entrypoint tar web cf - -C /usr/lib/python3/dist-packages --exclude=static --exclude=i18n --exclude=i18n_extra --exclude='l10n_*' --exclude='*.po' --exclude='*.pot' --exclude=demo --exclude=__pycache__ odoo | tar xf - -C .odoo-src
```

Karena `.vscode/` di-ignore, tambahkan sendiri di settings editor, mis. VS Code:

```json
{ "python.analysis.extraPaths": ["./.odoo-src"] }
```

Lint (opsional, perlu Python 3.11):

```bash
python3.11 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pylint --rcfile=.pylintrc custom_addons/starter_cats
```

## Troubleshooting

- **Port 8069 terpakai**: ubah `ODOO_PORT` di `.env`, lalu `docker compose up -d`.
- **Docker belum menyala**: jalankan Docker Desktop / daemon dulu.
- **`variable is missing a value`**: `.env` belum dibuat atau belum diisi.
- **Skrip `.sh` error `Permission denied` atau `\r`**: jalankan `chmod +x scripts/*.sh`; pastikan file memakai LF (`.gitattributes` sudah mengaturnya, clone ulang bila perlu).
- **Windows**: gunakan skrip `.cmd` dari Command Prompt, atau jalankan `.sh` di WSL.
- **Modul tidak muncul di Apps**: aktifkan Developer Mode, lalu **Apps → Update Apps List**.

## Versi

Odoo 17 (`odoo:17`) dan PostgreSQL 16 (`postgres:16-alpine`). Image ditandai dengan tag; naikkan versinya secara sengaja, bukan otomatis.

## Keamanan: development vs deployment

Konfigurasi di repository ini untuk development lokal: kredensial dari `.env` (jangan di-commit), database tidak membuka port ke host, dan `admin_passwd` (master password database manager) sengaja tidak diset. Untuk deployment, mulai dari `config/odoo.prod.conf.example` (set `admin_passwd`, `list_db = False`, `proxy_mode`, worker, batas memori) dan jangan memakai `--dev`.
