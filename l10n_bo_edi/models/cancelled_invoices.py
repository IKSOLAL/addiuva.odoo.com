from odoo import fields, models


class CancelledInvoices(models.Model):
    _name = 'cancelled_invoices'
    _description = 'SIN cancelled invoices'
    _rec_name = 'invoice_num' ## Para cambiar el texto a desplegar en front

    # payment_reference = fields.Char('payment_reference')

    invoice_num = fields.Integer(string='Invoice Number')
    
    invoice_dosage_id = fields.Many2one(comodel_name='invoice_dosage', string='Invoice Dosage Related')

    # display_name = fields.Char(string='Disp Name', compute='_compute_fields_combination')

    # @api.depends('invoice_num', 'invoice_dosage_id')
    # def _compute_fields_combination(self):
    #     for test in self:
    #         test.combination = test.field1 + ' ' + test.field2

    inv_reversed = fields.Boolean('reversed')

    reason_id = fields.Many2one(
        'cancellation_reasons', string='Cancellation Reason')

    date = fields.Datetime('Date')

    account_move_id = fields.Many2one(comodel_name='account.move', string='Invoice Related')
    

    active = fields.Boolean(
        'Active', help='Allows you to hide the cancelled invoice without removing it.', default=True)
