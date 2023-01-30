# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    payment_date_banking = fields.Date(string="Payment Date For Banking Report", required=True,
    default=fields.Date.context_today)

    transaction_reference = fields.Char(
        string="Transaction Reference for Banking Report",
        help="This value is used for Banking Report ",
    )

    def _create_payment_vals_from_wizard(self):
        # OVERRIDE
        payment_vals = super()._create_payment_vals_from_wizard()
        payment_vals['payment_date_banking'] = self.payment_date_banking
        payment_vals['transaction_reference'] = self.transaction_reference
        return payment_vals
