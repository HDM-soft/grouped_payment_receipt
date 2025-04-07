from odoo import models, fields, api


class AccountPaymentReceipt(models.Model):
    _name = "account.payment.receipt"
    _description = "Grouped Payment Receipt"
    _order = "date desc, id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Receipt Number", required=True, copy=False, readonly=True, default="New"
    )
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    payment_ids = fields.Many2many("account.payment", string="Payments", required=True)
    payment_names = fields.Char(
        string="Original Payments", compute="_compute_payment_names", store=True
    )
    move_ids = fields.Many2many("account.move", string="Invoices", required=True)
    company_id = fields.Many2one(
        "res.company", string="Company", compute="_compute_company", store=True
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", compute="_compute_currency", store=True
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("posted", "Posted"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
    )

    @api.depends("payment_ids")
    def _compute_payment_names(self):
        for record in self:
            record.payment_names = (
                ", ".join(record.payment_ids.mapped("name"))
                if record.payment_ids
                else ""
            )

    @api.depends("payment_ids")
    def _compute_company(self):
        for record in self:
            record.company_id = (
                record.payment_ids[:1].company_id if record.payment_ids else False
            )

    @api.depends("company_id")
    def _compute_currency(self):
        for record in self:
            record.currency_id = (
                record.company_id.currency_id if record.company_id else False
            )

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = (
                self.env["ir.sequence"].next_by_code("account.payment.receipt") or "New"
            )
        return super(AccountPaymentReceipt, self).create(vals)

    def action_post(self):
        self.write({"state": "posted"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_draft(self):
        self.write({"state": "draft"})

    def action_print_receipt(self):
        """Reimprime el recibo."""
        return self.env.ref(
            "grouped_payment_receipt.action_report_payment_receipt"
        ).report_action(self)
