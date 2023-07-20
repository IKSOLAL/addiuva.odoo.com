from odoo import models, fields, api

class res_company(models.Model):
    _inherit = ["res.company"]

    is_addiuva = fields.Boolean(string="Activa si esta empresa es ADDIUVA")