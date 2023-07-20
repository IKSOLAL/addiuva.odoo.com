# -*- coding: utf-8 -*-

from odoo import models, fields


class SoaIntegrationApi(models.Model):
    _inherit = 'account.analytic.account'

    product_plan_id = fields.Many2one(comodel_name="product.planes", string="PLAN")
    cod_soa = fields.Integer(related="product_plan_id.cod_soa", string='Código SOA')