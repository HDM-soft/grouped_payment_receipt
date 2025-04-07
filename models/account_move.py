from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_generate_grouped_payment_receipt(self):
        """Genera un reporte agrupado de pagos conciliados con las facturas seleccionadas (clientes o proveedores)."""
        partner_ids = self.mapped("partner_id")
        if len(partner_ids) > 1:
            raise UserError(
                "Por favor, selecciona facturas del mismo cliente o proveedor."
            )

        reconciled_lines = self.line_ids.filtered(lambda l: l.reconciled)
        if not reconciled_lines:
            raise UserError(
                "No hay líneas reconciliadas en las facturas seleccionadas."
            )

        reconciliations = self.env["account.partial.reconcile"].search(
            [
                "|",
                ("debit_move_id", "in", reconciled_lines.ids),
                ("credit_move_id", "in", reconciled_lines.ids),
            ]
        )

        payment_lines = self.env["account.move.line"]
        for rec in reconciliations:
            payment_lines |= (
                rec.credit_move_id
                if rec.debit_move_id in reconciled_lines
                else rec.debit_move_id
            )

        payment_ids = (
            payment_lines.mapped("move_id")
            .filtered(lambda m: m.is_payment())
            .mapped("payment_id")
        )

        if not payment_ids:
            raise UserError("No hay pagos conciliados para las facturas seleccionadas.")

        grouped_data = {}
        for payment in payment_ids:
            key = (payment.partner_id.id, payment.payment_date)
            if key not in grouped_data:
                grouped_data[key] = self.env["account.payment"]
            grouped_data[key] |= payment

        temp_records = self.env["account.payment.group.temp"].create(
            [
                {
                    "partner_id": partner_id,
                    "payment_date": payment_date,
                    "payment_ids": [(6, 0, payments.ids)],
                    "move_ids": [(6, 0, self.ids)],
                }
                for (partner_id, payment_date), payments in grouped_data.items()
            ]
        )

        return self.env.ref(
            "custom_payment_group_report.action_report_payment_group_receipt"
        ).report_action(temp_records)
