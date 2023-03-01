# -*- coding: utf-8 -*-

from odoo import models, fields


class IkAccountGroup(models.Model):
    _name = 'ik.account.group'

    name = fields.Char(string="Nombre")
    ik_company = fields.Many2one(comodel_name='res.company', string="Empresa",
                                 default=lambda self: self.env['res.company'].browse(self.env['res.company']._company_default_get('ik_account_group')))
    ik_account_ids = fields.One2many(comodel_name="account.account",inverse_name="ik_groups_account",string="Agrupacion de cuentas")













