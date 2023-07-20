from odoo import fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # internal_code = fields.Integer(string='Internal Code') # Currently using "Internal Reference"

    sin_item = fields.Many2one('sin_items', string='SIN Item related')

    measure_unit = fields.Many2one(
        'measure_unit', string='SIN Measure Unit related')
    
    internal_code = fields.Integer(string='Internal Code') # Electronic Invoice ID

