# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'File that executes modifications to the res.users model'

    category_id = fields.Many2many(comodel_name='res.partner.category', string='Categorias',
                                   help='Selecciona una categoria')
