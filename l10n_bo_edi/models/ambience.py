from odoo import fields, models


class Ambience(models.Model):
    _name = 'ambience'
    _description = 'ambience'

    id_ambience = fields.Integer(string='Ambiance Code')

    description = fields.Text(string='Description')

    current_ambience = fields.One2many(
        'res.config.settings', 'l10n_bo_ambience', string='Current Ambience')

    active = fields.Boolean(
        'Active', help='Allows you to hide the ambiance without removing it.', default=True)
