from odoo import models, fields, api

class category(models.Model):
    _name = "product.services.plans"
    _rec_name = 'cod_soa'

    name = fields.Char(string="")
    cod_soa = fields.Integer(string='Código SOA', required=True)
    company_id = fields.Many2one(comodel_name='res.company', string="Empresa",
                                 default=lambda self: self.env['res.company'].browse(self.env['res.company']._company_default_get('ik_integrations_group')))
    plan_id = fields.Many2one('product.planes', string='Plan', required=True)
    prod_ids = fields.Many2many('product.template',  string='Servicios de Plan')