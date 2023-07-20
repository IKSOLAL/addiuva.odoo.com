# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class res_bank(models.Model):
    _inherit = 'res.bank'

    vat = fields.Char(string='VAT')
    
