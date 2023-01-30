# Copyright 2016-2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_date_banking = fields.Date(string="Payment Date For Banking Report", required=True,
    default=fields.Date.context_today)
    
    transaction_reference = fields.Char(
        string="Transaction Reference for Banking Report",
        help="This value is used for Banking Report ",
    )



