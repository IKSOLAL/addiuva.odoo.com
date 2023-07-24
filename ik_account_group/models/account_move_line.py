# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = 'account.move.line'


    ik_groups_account = fields.Many2one(related='account_id.ik_groups_account', string="Agrupación")
