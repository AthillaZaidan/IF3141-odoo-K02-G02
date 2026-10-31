{
    "name": "Starter Cats",
    "summary": "Contoh modul Odoo 17: model, security, view, data, dan test",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "author": "IF3141",
    "category": "Tools",
    "depends": ["base", "mail"],
    "application": True,
    # Urutan penting: security dulu (group dipakai ACL dan view), lalu view, lalu data.
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/cat_type_views.xml",
        "views/cat_views.xml",
        "views/menus.xml",
        "data/seed_data.xml",
    ],
    # Hanya dimuat jika DB dibuat tanpa --without-demo.
    "demo": ["demo/demo.xml"],
}
