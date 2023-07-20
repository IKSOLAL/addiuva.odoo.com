from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    l10n_bo_is_selling_point = fields.Boolean(
        string='E-Invoicing Selling Point')

    l10n_bo_selling_point_id = fields.Many2one(
        'selling_point', string='Selling Point')
