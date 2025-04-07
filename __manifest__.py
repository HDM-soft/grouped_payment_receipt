# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Grouped Payment Receipt",
    "summary": """
        Generates a grouped PDF receipt report for payments posted with selected customer or vendor payments.""",
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "17.0.12.10.0",
    "development_status": "Production/Stable",
    "depends": ["account", "l10n_ar"],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/report_payment_receipt.xml",
        "views/account_payment_actions.xml",
        "views/account_payment_receipt_views.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
