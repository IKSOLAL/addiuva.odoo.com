# -*- coding: utf-8 -*-

from odoo import models,fields,api


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    check_number = fields.Char(string="Número de cheque")

    show_check_number = fields.Boolean(string="Show Check Number")

    @api.onchange('payment_method_line_id')
    def _compute_show_check_number(self):
        for wizard in self:
            wizard.show_check_number = False
            if wizard.payment_method_line_id.name == 'Cheques' or wizard.payment_method_line_id.name == 'Checks':
                wizard.show_check_number = True

    def _create_payments(self):
        payments = super()._create_payments()
        for p in payments:
            try:
                p.check_number = self.check_number
            except:
                return payments
        return payments

