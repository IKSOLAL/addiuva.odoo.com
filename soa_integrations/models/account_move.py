from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = ["account.move"]

    cod_soa = fields.Integer(string="Código SOA", required=True, default=0)
    payment_module_soa = fields.Boolean(string="Modulo Pagos SOA", default=0)