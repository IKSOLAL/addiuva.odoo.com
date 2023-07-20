from odoo import fields, models, api


class IdType(models.Model):
    _name = 'id_type'
    _description = 'Client ID type'
    _rec_name = 'description' ## Para cambiar el texto a desplegar en front

    id_type_code = fields.Integer(string='ID Type Code')

    description = fields.Text(string='Description')

    res_partner_ids = fields.One2many(
        'res.partner', 'l10n_bo_id_type', string='Related Clients')

    active = fields.Boolean(
        'Active', help='Allows you to hide the id type without removing it.', default=True)
