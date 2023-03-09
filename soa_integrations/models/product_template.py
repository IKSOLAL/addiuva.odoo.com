from odoo import models, fields, api

class product_template(models.Model):
    _inherit = ["product.template"]

    plan_id = fields.Many2one('product.planes', string="Plan")

