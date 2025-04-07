from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_generate_grouped_payment_receipt(self):
        """Genera un reporte agrupado de pagos conciliados con las facturas seleccionadas (clientes o proveedores)."""
        # Verificar que todas las facturas sean del mismo partner
        partner_ids = self.mapped("partner_id")
        if len(partner_ids) > 1:
            raise UserError(
                "Por favor, selecciona facturas del mismo cliente o proveedor."
            )

        # Obtener todas las líneas de las facturas que tienen reconciliaciones parciales
        all_lines = self.line_ids
        reconciliations = self.env["account.partial.reconcile"].search(
            [
                "|",
                ("debit_move_id", "in", all_lines.ids),
                ("credit_move_id", "in", all_lines.ids),
            ]
        )

        if not reconciliations:
            raise UserError(
                "No hay líneas reconciliadas en las facturas seleccionadas."
            )

        # Identificar las líneas de la factura que tienen reconciliaciones
        reconciled_lines = self.env["account.move.line"]
        for rec in reconciliations:
            if rec.debit_move_id in all_lines:
                reconciled_lines |= rec.debit_move_id
            if rec.credit_move_id in all_lines:
                reconciled_lines |= rec.credit_move_id

        # Identificar las líneas de pago asociadas a las reconciliaciones
        payment_lines = self.env["account.move.line"]
        for rec in reconciliations:
            payment_lines |= (
                rec.credit_move_id
                if rec.debit_move_id in reconciled_lines
                else rec.debit_move_id
            )

        # Filtrar movimientos que son pagos usando payment_id
        payment_moves = payment_lines.mapped("move_id").filtered(lambda m: m.payment_id)
        payment_ids = payment_moves.mapped("payment_id")

        if not payment_ids:
            raise UserError("No hay pagos conciliados para las facturas seleccionadas.")

        # Agrupar pagos por partner y fecha
        grouped_data = {}
        for payment in payment_ids:
            key = (payment.partner_id.id, payment.date)
            if key not in grouped_data:
                grouped_data[key] = self.env["account.payment"]
            grouped_data[key] |= payment

        # Crear registros temporales para el reporte
        temp_records = self.env["account.payment.group.temp"].create(
            [
                {
                    "partner_id": partner_id,
                    "date": date,
                    "payment_ids": [(6, 0, payments.ids)],
                    "move_ids": [(6, 0, self.ids)],
                }
                for (partner_id, date), payments in grouped_data.items()
            ]
        )

        # Generar el reporte
        return self.env.ref(
            "custom_payment_group_report.action_report_payment_group_receipt"
        ).report_action(temp_records)
