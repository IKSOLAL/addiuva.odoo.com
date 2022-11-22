from odoo import fields, models


class Modalities(models.Model):
    _name = 'modalities'
    _description = 'modalities'

    id_modality = fields.Integer(string='Modality Code')

    description = fields.Text(string='Description')

    current_invoicing_modality = fields.One2many(
        'res.config.settings', 'l10n_bo_invoicing_modality', string='Current Invoicing Modality')

    active = fields.Boolean(
        'Active', help='Allows you to hide the modality without removing it.', default=True)
