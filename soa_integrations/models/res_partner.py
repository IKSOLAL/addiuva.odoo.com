from odoo import models, fields, api

class res_company(models.Model):
    _inherit = "res.partner"

    soa_local = fields.Boolean(string="SOA Local")
    soa_country = fields.Many2one(comodel_name="res.country",string="SOA Pais")