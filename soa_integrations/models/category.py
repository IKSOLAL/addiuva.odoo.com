from odoo import models, fields, api

class category(models.Model):
    _inherit = ["product.category"]

    company_id = fields.Many2one('res.company' , string="Company")