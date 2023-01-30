from odoo import models, fields, api

class InvoiceCancelReason(models.TransientModel):
    _name = "invoice_cancel_reason_wizard"
    _description = "SIN invoice cancellation reasons in a popup"

    cancellation_reason_id = fields.Many2one('cancellation_reasons', string='Cancellation Reason')
    
    def cancel_invoice(self):
        self.env['account.move'].invoice_cancellation(self._context.get('cufd'), self._context.get('cuf'), self.cancellation_reason_id.code)
