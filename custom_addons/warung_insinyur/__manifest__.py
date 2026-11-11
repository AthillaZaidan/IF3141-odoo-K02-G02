{
    "name": "Warung Insinyur - Stok dan Pelaporan",
    "summary": "Konfigurasi Inventory, Purchase, dan BoM kit untuk Warung Insinyur (prototipe IF3141 K02-G02)",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "author": "IF3141 K02-G02",
    "category": "Inventory/Inventory",
    "depends": [
        "stock",
        "purchase_stock",
        "mrp",
        "l10n_id",  # chart of accounts Indonesia -> mata uang perusahaan IDR
        "spreadsheet_dashboard_stock_account",
        "spreadsheet_dashboard_purchase_stock",
    ],
    "data": [
        "data/company_settings.xml",
        "data/locations.xml",
        "data/partners.xml",
        "data/products_bahan.xml",
        "data/products_menu.xml",
        "data/bom_takaran.xml",
        "data/orderpoints.xml",
        "data/users.xml",
        "data/pelaporan_access.xml",
    ],
    "application": False,
}
