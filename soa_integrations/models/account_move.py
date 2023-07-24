from odoo import models, fields, api
import requests

class AccountMove(models.Model):
    _inherit = ["account.move"]

    cod_soa = fields.Integer(string="Código SOA", required=True, default=0)
    payment_module_soa = fields.Boolean(string="Modulo Pagos SOA", default=0)
    paid = fields.Boolean(string="Pagada")

    @api.onchange('payment_state')
    def onchange_state(self):
        for invoice in self:
            invoice.sync_soa(invoice.payment_state)
                

    def sync_soa(self,payment_state):
        if payment_state == 'paid':
            response = requests.put('https://api.sistemaoperaciones.com/payment-provider/invoice/odoo-update-status/'+self.cod_soa+'/', data = {'IvStatus':'5'})


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