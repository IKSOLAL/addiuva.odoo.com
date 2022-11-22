from odoo import fields, models


class CancellationReasons(models.Model):
    _name = 'cancellation_reasons'
    _description = 'cancellation_reasons'
    _rec_name = 'description' ## Para cambiar el texto a desplegar en front

    code = fields.Integer('code')

    description = fields.Text('description')

    active = fields.Boolean(
        'Active', help='Allows you to hide the cancellation reasons without removing it.', default=True)
