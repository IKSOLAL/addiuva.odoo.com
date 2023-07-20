from odoo import fields, models


class Cufd_log(models.Model):
    _name = 'cufd_log'
    _description = 'cufd'
    _rec_name = 'id_cufd' ## Para cambiar el texto a desplegar en front

    id_cufd = fields.Integer(string='Cufd ID')

    cufd = fields.Text(string='CUFD')

    controlCode = fields.Text(string='Control Code')

    begin_date = fields.Datetime(string='Begin Date')

    end_date = fields.Datetime(string='End Date')

    invoice_number = fields.Integer(string='Invoice Number')

    selling_point = fields.Many2one('selling_point', string='Selling Point')

    active = fields.Boolean(
        'Active', help='Allows you to hide the cufd without removing it.', default=True)
