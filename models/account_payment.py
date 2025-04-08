from odoo import models, api
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_generate_grouped_payment_receipt(self):
        """Generate a grouped payment receipt from the selected payments.

        Raises:
            UserError: If payments belong to different partners or if no posted payments are selected.
        """
        # Ensure all payments belong to the same partner
        partner_ids = self.mapped("partner_id")
        if len(partner_ids) > 1:
            raise UserError("Please select payments from the same customer or vendor.")

        # Filter only posted payments
        posted_payments = self.filtered(lambda p: p.state == "posted")
        if not posted_payments:
            raise UserError("There are no posted payments to generate the receipt.")

        # Get invoices associated with the payments
        invoices = self.env["account.move"]
        for payment in posted_payments:
            payment_lines = payment.move_id.line_ids.filtered(
                lambda l: l.account_id.account_type
                in ("asset_receivable", "liability_payable")
            )
            reconciliations = self.env["account.partial.reconcile"].search(
                [
                    "|",
                    ("debit_move_id", "in", payment_lines.ids),
                    ("credit_move_id", "in", payment_lines.ids),
                ]
            )
            for reconciliation in reconciliations:
                invoice = (
                    reconciliation.credit_move_id.move_id
                    if reconciliation.debit_move_id in payment_lines
                    else reconciliation.debit_move_id.move_id
                )
                if invoice.is_invoice():
                    invoices |= invoice

        # Group payments by partner and date
        grouped_data = {}
        for payment in posted_payments:
            key = (payment.partner_id.id, payment.date)
            if key not in grouped_data:
                grouped_data[key] = self.env["account.payment"]
            grouped_data[key] |= payment

        # Create grouped payment receipt records
        receipt_records = self.env["account.payment.receipt"].create(
            [
                {
                    "partner_id": partner_id,
                    "date": payment_date,
                    "payment_ids": [(6, 0, payments.ids)],
                    "move_ids": [(6, 0, invoices.ids)],
                    "state": "posted",
                }
                for (partner_id, payment_date), payments in grouped_data.items()
            ]
        )

        return self.env.ref(
            "grouped_payment_receipt.action_report_payment_receipt"
        ).report_action(receipt_records)
