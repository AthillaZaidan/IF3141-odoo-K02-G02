"""Saldo stok awal (data uji) dan bahasa antarmuka.

Saldo awal dicatat lewat inventory adjustment bawaan Odoo agar riwayat stok
mencatatnya sebagai penyesuaian awal (IW-05), bukan data yang disisipkan langsung.
"""

# (xml id bahan, xml id lokasi, jumlah awal) -- DATA UJI
SALDO_AWAL = [
    ("bhn_indomie_goreng", "loc_kitchen", 80),
    ("bhn_indomie_kuah", "loc_kitchen", 40),
    ("bhn_telur", "loc_kitchen", 60),
    ("bhn_kornet", "loc_kitchen", 0.8),  # sengaja di bawah minimum (1 kg) untuk uji FR-09
    ("bhn_bawang_merah", "loc_kitchen", 1),
    ("bhn_kerupuk", "loc_kitchen", 100),
    ("bhn_beras", "loc_gudang", 10),
    ("bhn_minyak", "loc_gudang", 4),
    ("bhn_cincau", "loc_bar", 3),
    ("bhn_gula_aren", "loc_bar", 2),
    ("bhn_santan", "loc_bar", 2),
    ("bhn_es_batu", "loc_bar", 4),  # sengaja di bawah minimum (5 kg) untuk uji FR-09
]


def post_init_hook(env):
    # CR-4: mata uang Rupiah. Diset di sini (bukan hanya XML) karena instalasi
    # modul akuntansi bawaan dapat mengembalikan mata uang perusahaan ke USD.
    env.ref("base.main_company").currency_id = env.ref("base.IDR")

    quants = env["stock.quant"]
    for product_xmlid, location_xmlid, qty in SALDO_AWAL:
        product = env.ref(f"warung_insinyur.{product_xmlid}").product_variant_id
        location = env.ref(f"warung_insinyur.{location_xmlid}")
        quants |= quants.with_context(inventory_mode=True).create({
            "product_id": product.id,
            "location_id": location.id,
            "inventory_quantity": qty,
        })
    quants.action_apply_inventory()

    # QR-9 / CR-4: antarmuka berbahasa Indonesia bila bahasa id_ID sudah dimuat.
    if env["res.lang"]._lang_get("id_ID"):
        users = env.ref("base.user_admin") | env["res.users"].search(
            [("login", "like", "@warunginsinyur.test")]
        )
        users.write({"lang": "id_ID"})
