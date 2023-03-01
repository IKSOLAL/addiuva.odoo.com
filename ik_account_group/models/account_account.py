# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = 'account.account'

    ik_groups_account = fields.Many2one(comodel_name='ik.account.group', string="Agrupacion")
