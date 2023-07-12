from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = ["purchase.order"]

    support_num_soa = fields.Char(string="SOA No. Soporte")
    cod_soa = fields.Integer(string='Código SOA', required=True, default=0)
    record_num_soa = fields.Char(string="SOA No. Expediente")
    product_service_plan_id = fields.Many2one(comodel_name="product.services.plans",string="Plan-Servicio")

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    plan_id = fields.Many2one(comodel_name="product.planes",string="Plan")


    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        for line in self:
            analytic = self.env['account.analytic.account'].search([('product_plan_id','=',line.plan_id.id)])
            if analytic:
                line.account_analytic_id = analytic.id
            else:
                raise UserError("El plan no tiene una cuenta analitica asociada")
    