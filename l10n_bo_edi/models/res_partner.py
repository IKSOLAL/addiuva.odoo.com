from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from string import digits


class ResPartner (models.Model):
    _inherit = 'res.partner'
    _description = 'Partner Inherit BO EDI'

    l10n_bo_id_type = fields.Many2one('id_type', string='ID Type')

    complement = fields.Text(string='Complement')
    
    @api.constrains('vat')
    def _check_vat(self):
        for record in self:
            if not record.vat:
                raise ValidationError('VAT value is not valid')
    
    ##TODO Pendiente adecuación para registro en backend
