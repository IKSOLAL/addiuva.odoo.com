# -*- coding: utf-8 -*-

from odoo import models, fields


class SoaIntegrationApi(models.Model):
    _inherit = 'account.analytic.account'

    product_service_plan_id = fields.Many2one(comodel_name="product.services.plans", string="Plan-Servicio")
    cod_soa = fields.Integer(string='Código SOA', required=True, default=0)