# warung_insinyur

Modul konfigurasi untuk **Sistem Pengelolaan Stok dan Pelaporan Operasional Terintegrasi Berbasis Odoo** (IF3141 K02-G02). Modul ini tidak menambah model baru. Isinya hanya konfigurasi modul bawaan Odoo 17 dan **data uji (simulasi)**.

| File | Isi | Rujukan M3 |
|---|---|---|
| `data/company_settings.xml` | Nama perusahaan, IDR, pengaturan multi-lokasi dan satuan | CR-4 |
| `data/locations.xml` | Lokasi WH/Stock/Kitchen, Bar, Gudang | IW-01 |
| `data/partners.xml` | Supplier Grup Hotel (data uji) | IW-02, FR-02 |
| `data/products_bahan.xml` | 12 bahan (BHN-001..012) + harga beli dari supplier | IW-01, FR-01 |
| `data/products_menu.xml` | 6 menu (MN-001..006) | IW-03 |
| `data/bom_takaran.xml` | Takaran bahan per menu sebagai BoM jenis kit | FR-03 |
| `data/orderpoints.xml` | Batas stok minimum/maksimum per bahan dan lokasi | FR-09, IW-04 |
| `data/users.xml` | 5 akun sesuai peran (hak ekspor hanya Owner dan Supervisor) | FR-13, FR-12, IW-12 |
| `data/pelaporan_access.xml` | Grup "Pelaporan Operasional": dasbor hanya untuk Owner, Supervisor, Head Store | FR-11, QR-2 |
| `hooks.py` | Saldo stok awal (lewat inventory adjustment) dan bahasa Indonesia | IW-05, QR-9 |
| `sample/*.csv` | Contoh berkas impor penjualan harian (valid dan galat) | FR-06 |

## Install

```bash
docker compose up -d
docker compose run --rm web odoo -d odoo_app --load-language=id_ID -i warung_insinyur --stop-after-init
docker compose restart web
```

Ketergantungan: `stock`, `purchase_stock`, `mrp`, `l10n_id` (chart of accounts Indonesia, supaya mata uang perusahaan IDR), serta dasbor bawaan `spreadsheet_dashboard_stock_account` dan `spreadsheet_dashboard_purchase_stock`.

Install pada database kosong. Modul membuat saldo awal stok dan menjalankan data uji, jadi jangan dipasang di database yang sudah berisi data nyata.

## Akun uji (lokal saja)

| Peran | Login | Kata sandi |
|---|---|---|
| Owner | owner@warunginsinyur.test | owner12345 |
| Supervisor | supervisor@warunginsinyur.test | supervisor12345 |
| Head Store | headstore@warunginsinyur.test | headstore12345 |
| Kasir | kasir@warunginsinyur.test | kasir12345 |
| Penanggung Jawab Stok | pjstok@warunginsinyur.test | pjstok12345 |

## Impor penjualan harian (FR-06, FR-07)

1. Inventaris › Operasi › Transfer › Pengiriman › ikon gerigi › **Impor record**, unggah CSV dengan format `sample/penjualan_2026-11-20.csv`.
2. Kolom `id` berisi `penjualan_<tanggal>`. Impor ulang tanggal yang sama ditolak sehingga data tidak tergandakan (QR-1).
3. Nama menu di berkas harus sama dengan nama menu di Odoo. Nama yang tidak dikenal (contoh `sample/penjualan_2026-11-21_galat.csv`) ditolak dengan pesan galat.
4. Buka transfer hasil impor › **Tandai sebagai Akan Dilakukan**: setiap menu terurai menjadi bahan sesuai BoM kit (pemakaian teoretis) › **Validasi**: stok bahan berkurang.

Nama bahan dan nama menu harus berbeda (mis. bahan "Mi Instan Indomie Goreng (bungkus)" vs menu "Indomie Goreng"), karena impor mencari produk berdasarkan nama.
