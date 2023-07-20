from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = ["account.move"]

    cod_soa = fields.Integer(string="Código SOA", required=True, default=0)
    payment_module_soa = fields.Boolean(string="Modulo Pagos SOA", default=0)

    def sync_soa(self):
        print("test")


class AccountMoveLine(models.Model):
    _inherit = ["account.move.line"]


    plan_id = fields.Many2one(comodel_name="product.planes",string="Plan")

    @api.model
    def create(self,vals):
        line = super(AccountMoveLine,self).create(vals)
        analytic = self.env['account.analytic.account'].search([('product_plan_id','=',line.plan_id.id)],limit=1)
        if analytic:
            if line.account_id.user_type_id.property_analytic_policy != 'never':
                line.analytic_account_id = analytic.id
        else:
            raise UserError("El plan no tiene una cuenta analitica asociada")

        return line

    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        for line in self:
            analytic = self.env['account.analytic.account'].search([('product_plan_id','=',line.plan_id.id)],limit=1)
            if analytic:
                line.analytic_account_id = analytic.id
            else:
                raise UserError("El plan no tiene una cuenta analitica asociada")