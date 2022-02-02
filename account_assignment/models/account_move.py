# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    assignment = fields.Char(string="Asignacion")
