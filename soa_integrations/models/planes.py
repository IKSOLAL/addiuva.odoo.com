from odoo import models, fields, api

class category(models.Model):
    _name = "product.planes"

    name = fields.Char(string="Plan")