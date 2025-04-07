from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_generate_grouped_payment_receipt(self):
        """Genera un reporte agrupado de pagos conciliados con las facturas seleccionadas (clientes o proveedores)."""
        # Validar que todas las facturas sean del mismo partner
        partner_ids = self.mapped("partner_id")
        if len(partner_ids) > 1:
            raise UserError(
                "Por favor, selecciona facturas del mismo cliente o proveedor."
            )

        # Obtener los pagos conciliados con las líneas de las facturas
        payment_ids = self.env["account.payment"]
        for move in self:
            reconciled_lines = move.line_ids.filtered(lambda l: l.reconciled)
            payment_ids |= reconciled_lines.mapped("matched_payment_ids")

        if not payment_ids:
            raise UserError("No hay pagos conciliados para las facturas seleccionadas.")

        # Agrupar pagos por partner y fecha
        grouped_data = {}
        for payment in payment_ids:
            key = (payment.partner_id.id, payment.payment_date)
            if key not in grouped_data:
                grouped_data[key] = self.env["account.payment"]
            grouped_data[key] |= payment

        # Crear registros temporales para el reporte
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

        # Retornar la acción del reporte
        return self.env.ref(
            "custom_payment_group_report.action_report_payment_group_receipt"
        ).report_action(temp_records)
