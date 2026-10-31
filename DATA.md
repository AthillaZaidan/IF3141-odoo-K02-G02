# DATA.md — Pemetaan Data Pribadi

> Dokumen ini adalah pemetaan awareness untuk tugas besar, **bukan opini hukum**.
> Isi tabel di bawah dengan data yang benar-benar disimpan oleh sistem kelompok Anda.
> Baris contoh berasal dari Odoo standar dan modul `starter_cats`; hapus atau ganti sesuai sistem Anda.

## Data pribadi yang disimpan

| Entitas (model) | Field | Benar-benar perlu? | Tujuan | Siapa yang boleh mengakses |
|---|---|---|---|---|
| Pengguna (`res.users`) | nama, login (email) | Ya | Autentikasi dan pencatatan siapa melakukan apa | Administrator; pemilik akun (data sendiri) |
| Kontak (`res.partner`) | nama, email, telepon, alamat | _Isi: tentukan per kasus_ | _Isi_ | _Isi: group/role_ |
| Chatter (`mail.message`) | penulis, isi pesan | _Isi_ | Jejak komunikasi pada record | Pengguna yang bisa mengakses record terkait |
| Kucing (`starter.cat`) | `create_uid` (pembuat) | Ya | Record rule: user hanya melihat data buatannya | Pembuat; Manager |
| _(tambahkan entitas sistem Anda)_ | | | | |

## Siklus data

| Tahap | Apa yang dilakukan sistem kita | Kontrol atau bukti |
|---|---|---|
| Pemerolehan / pengumpulan | _Isi: dari mana data masuk (form, impor, API)_ | _Isi: mis. field wajib, validasi, persetujuan_ |
| Pengolahan / penganalisisan | _Isi: proses/laporan yang memakai data_ | _Isi: mis. hak akses per group_ |
| Penyimpanan | PostgreSQL (volume `odoo-db-data`) dan filestore (volume `odoo-web-data`); kredensial dari `.env` yang tidak di-commit | `.gitignore` menolak `.env` dan dump; `db` tidak membuka port ke host |
| Perbaikan / pembaruan | _Isi: siapa dan bagaimana data dikoreksi_ | Tracking chatter (`tracking=True`) mencatat perubahan field |
| Penampilan / pengumuman / transfer / penyebarluasan / pengungkapan | _Isi: view, laporan, ekspor, backup yang berpindah antar anggota tim_ | ACL + record rule; dump di `dump/` tidak di-commit |
| Penghapusan / pemusnahan | _Isi: kapan dan bagaimana data dihapus_ | _Isi: mis. `docker compose down -v`, prosedur hapus record, retensi_ |

## Jika terjadi kegagalan pelindungan data

Siapa yang memberi tahu, dan lewat apa:

- Pihak yang memberi tahu: _Isi (nama peran, bukan hanya nama orang)_
- Kepada siapa: _Isi (pemilik data, dosen/asisten, pihak perusahaan)_
- Saluran: _Isi (email, chat, telepon)_
- Batas waktu internal: _Isi_

## Penanggung jawab sistem di perusahaan

- Peran / jabatan: _Isi_
- Kontak: _Isi_
