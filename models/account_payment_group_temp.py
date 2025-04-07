from odoo import models, fields, api


class AccountPaymentGroupTemp(models.AbstractModel):
    _name = "account.payment.group.temp"
    _description = "Temporary model for grouped payment receipt"
    _auto = False  # No crea tabla en la base de datos

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    date = fields.Date(string="Payment Date", required=True)
    # Reemplazamos Many2many por una lista de IDs que pasaremos al reporte
    payment_ids_list = fields.Binary(
        string="Payment IDs", readonly=True
    )  # Almacenamos IDs como datos
    move_ids_list = fields.Binary(
        string="Move IDs", readonly=True
    )  # Almacenamos IDs como datos
    company_id = fields.Many2one(
        "res.company", string="Company", compute="_compute_company"
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", compute="_compute_currency"
    )
    amount_total = fields.Monetary(
        string="Total Amount",
        compute="_compute_amount_total",
        currency_field="currency_id",
    )

    @api.depends("payment_ids_list")
    def _compute_company(self):
        for record in self:
            payment_ids = record.payment_ids_list or []
            if payment_ids:
                payment = record.env["account.payment"].browse(payment_ids[0])
                record.company_id = payment.company_id
            else:
                record.company_id = False

    @api.depends("company_id")
    def _compute_currency(self):
        for record in self:
            record.currency_id = (
                record.company_id.currency_id if record.company_id else False
            )

    @api.depends("payment_ids_list")
    def _compute_amount_total(self):
        for record in self:
            payment_ids = record.payment_ids_list or []
            payments = record.env["account.payment"].browse(payment_ids)
            record.amount_total = sum(payment.amount for payment in payments)
