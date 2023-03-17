from odoo import models, fields, api

class product_template(models.Model):
    _inherit = ["product.template"]

    plan_servicio_ids = fields.Many2many("product.services.plans", string="Planes")
    cod_soa = fields.Integer(string='Código SOA', required=True)
    company_id = fields.Many2one(comodel_name='res.company', string="Empresa",
                                 default=lambda self: self.env['res.company'].browse(
                                     self.env['res.company']._company_default_get('ik_integrations_group')))

