from odoo import models, fields, api
from odoo.exceptions import UserError, Warning, ValidationError
import logging

_logger = logging.getLogger(__name__)

class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"
    _description = "Account move reversal inherit"

    cancellation_reason_id = fields.Many2one('cancellation_reasons', string='Cancellation Reason')
    
    def get_invoice_type(self):
        self.inv_type = self._context.get('inv_type')
    inv_type = fields.Boolean(compute="get_invoice_type")

    def reverse_moves(self):
        _logger.info("/////////////INGRESO ANULACIÓN FACTURA///////////////")
        _logger.info('CONTEXTO: ' + str(self._context))
        if self._context.get('inv_type'):
            if not self.cancellation_reason_id:
                raise ValidationError("You must select a cancellation reason, in order to send it to SIN")
            if self.refund_method != 'cancel':
                raise ValidationError("You must select Full refund option in E-Billing modality")
        
        ## Cambiar flag cancel active para registro automatico de reversa y luego retornar a valor 0:
        cancel_flag = self.env['bo_edi_params'].search(
            [('name', '=', 'CANCEL_ACTIVE')])
        cancel_flag.write({"value" : 1})
        super(AccountMoveReversal, self).reverse_moves()
        cancel_flag.write({"value" : 0})

        if self._context.get('external'):
            self.env['account.move'].null_invoice(self._context.get('account_move_id'), self.cancellation_reason_id.code)
        else:                                                  
            self.env['account.move'].invoice_cancellation(self._context.get('inv_type'),
                                                        self._context.get('cufd'),
                                                        self._context.get('cuf'), 
                                                        self._context.get('inv_number'), 
                                                        self._context.get('account_move_id'), 
                                                        self._context.get('invoice_dosage_id'),
                                                        self.cancellation_reason_id.code,
                                                        self._context.get('email_to'))

