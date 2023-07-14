from odoo import models, fields, api

class category(models.Model):
    _name = "product.planes"

    partner_id = fields.Many2one(comodel_name="res.partner",string="Cliente")
    name = fields.Char(string="Plan", required=True)
    cod_soa = fields.Integer(string="Código SOA", required=True)
    company_id = fields.Many2one(comodel_name='res.company', string="Empresa",
                                 default=lambda self: self.env['res.company'].browse(self.env['res.company']._company_default_get('ik_integrations_group')))
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the plan without removing it.")

    @api.model
    def create(self,vals):
        new_product_plan = super(category,self).create(vals)
        #group_id:17 es Cecos Ingresos y Costos (objeto PA)
        account_vals = {
                'name': new_product_plan.name, 
                'product_plan_id': new_product_plan.id,
                'cod_soa': new_product_plan.cod_soa,
                'code':new_product_plan.cod_soa,
                'partner_id':new_product_plan.partner_id.id,
                'company_id':new_product_plan.company_id.id,
                'group_id':17,}
        account = self.env['account.analytic.account'].create(account_vals)
        return new_product_plan
     
 
