from odoo import models, fields, api

class category(models.Model):
    _inherit = ["product.category"]

    cod_soa = fields.Integer(string="Código SOA", required=True, default=0)
    company_id = fields.Many2one(comodel_name='res.company', string="Empresa",
                                 default=lambda self: self.env['res.company'].browse(self.env['res.company']._company_default_get('ik_integrations_group')))
    #company_id = fields.Many2one(comodel_name='res.company', string="Empresa", default=1)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the category without removing it.")
