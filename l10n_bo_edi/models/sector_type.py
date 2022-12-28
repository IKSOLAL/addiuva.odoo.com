from odoo import fields, models, api


class SectorType(models.Model):
    _name = 'sector_types'
    _description = 'Sector Type'

    id_sector_type = fields.Integer(string='ID Sector Type')

    description = fields.Text(string='Description')

    current_sector_type = fields.One2many(
        'res.config.settings', 'l10n_bo_sector_type', string='Current Sector Type')

    active = fields.Boolean(
        'Active', help='Allows you to hide the sector type without removing it.', default=True)
