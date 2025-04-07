from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_generate_grouped_payment_receipt(self):
        """Genera un recibo agrupado a partir de los pagos seleccionados."""
        # Verificar que todos los pagos sean del mismo partner
        partner_ids = self.mapped("partner_id")
        if len(partner_ids) > 1:
            raise UserError(
                "Por favor, selecciona pagos del mismo cliente o proveedor."
            )

        # Filtrar solo pagos publicados
        payments = self.filtered(lambda p: p.state == "posted")
        if not payments:
            raise UserError("No hay pagos publicados para generar el recibo.")

        # Obtener las facturas asociadas a los pagos
        move_ids = self.env["account.move"]
        for payment in payments:
            # Buscar las líneas del pago
            payment_lines = payment.move_id.line_ids.filtered(
                lambda l: l.account_id.account_type
                in ("asset_receivable", "liability_payable")
            )
            # Buscar reconciliaciones asociadas a esas líneas
            reconciliations = self.env["account.partial.reconcile"].search(
                [
                    "|",
                    ("debit_move_id", "in", payment_lines.ids),
                    ("credit_move_id", "in", payment_lines.ids),
                ]
            )
            # Obtener las facturas (account.move) asociadas
            for rec in reconciliations:
                if rec.debit_move_id in payment_lines:
                    move = rec.credit_move_id.move_id
                else:
                    move = rec.debit_move_id.move_id
                if move.is_invoice():
                    move_ids |= move

        # Agrupar pagos por partner y fecha
        grouped_data = {}
        for payment in payments:
            key = (payment.partner_id.id, payment.date)
            if key not in grouped_data:
                grouped_data[key] = self.env["account.payment"]
            grouped_data[key] |= payment

        # Crear registros de recibos agrupados
        receipt_records = self.env["account.payment.receipt"].create(
            [
                {
                    "partner_id": partner_id,
                    "date": payment_date,
                    "payment_ids": [(6, 0, payments.ids)],
                    "move_ids": [(6, 0, move_ids.ids)],
                    "state": "posted",
                }
                for (partner_id, payment_date), payments in grouped_data.items()
            ]
        )

        return self.env.ref(
            "grouped_payment_receipt.action_report_payment_receipt"
        ).report_action(receipt_records)
