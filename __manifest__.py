# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Grouped Payment Receipt from Invoices",
    "summary": """
        Generates a grouped PDF receipt report for payments reconciled with selected customer or vendor invoices.""",
    "author": "Be OnlyOne",
    "maintainers": ["onlyone-odoo"],
    "website": "https://onlyone.odoo.com/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "17.0.2.1.0",
    "development_status": "Production/Stable",
    "depends": ["account", "l10n_ar"],
    "data": [
        "views/report_payment_group.xml",
        "views/account_move_actions.xml",
    ],
    "application": False,
    "installable": True,
    "auto_install": False,
}
