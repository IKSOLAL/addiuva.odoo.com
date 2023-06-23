from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = ["purchase.order"]

    support_num_soa = fields.Char(string="SOA No. Soporte")
    cod_soa = fields.Integer(string='Código SOA', required=True, default=0)
    record_num_soa = fields.Char(string="SOA No. Expediente")
    product_service_plan_id = fields.Many2one(comodel_name="product.services.plans",string="Plan-Servicio")