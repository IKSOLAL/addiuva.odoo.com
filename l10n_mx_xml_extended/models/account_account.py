# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = 'account.account'

    include_uuid_edi = fields.Boolean(string="Incluir UUID XML Poliza",
                                      help="Incluir los UUID que se agreguen a la poliza")
