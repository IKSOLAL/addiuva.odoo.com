from odoo import fields, models


class Emission_types(models.Model):
    _name = 'emission_types'
    _description = 'emission_types'

    id_emission_type = fields.Integer(string='Emission_type Code')

    description = fields.Text(string='Description')

    current_emission_type = fields.One2many(
        'res.config.settings', 'l10n_bo_emission_type', string='Current Emission Type')

    active = fields.Boolean(
        'Active', help='Allows you to hide the emission_type without removing it.', default=True)
