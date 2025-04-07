from odoo import models, fields, api


class AccountPaymentGroupTemp(models.AbstractModel):
    _name = "account.payment.group.temp"
    _description = "Temporary model for grouped payment receipt"
    _auto = False

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    date = fields.Date(string="Payment Date", required=True)
    payment_ids = fields.Many2many("account.payment", string="Payments", required=True)
    move_ids = fields.Many2many("account.move", string="Invoices")
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

    @api.depends("payment_ids")
    def _compute_company(self):
        for record in self:
            record.company_id = record.payment_ids[:1].company_id

    @api.depends("company_id")
    def _compute_currency(self):
        for record in self:
            record.currency_id = record.company_id.currency_id

    @api.depends("payment_ids")
    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(record.payment_ids.mapped("amount"))
