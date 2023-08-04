from odoo import models, fields, api,_
import requests
from odoo.exceptions import UserError, Warning
import logging
import json
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = ["account.move"]

    cod_soa = fields.Integer(string="Código SOA", required=True, default=0)
    payment_module_soa = fields.Boolean(string="Modulo Pagos SOA", default=0)
    status_soa = fields.Selection([('paid','Pagada'),('not_paid','No Pagada')],string="Status SOA", compute='_status_soa')


                
    @api.onchange('payment_state','status_soa')
    def _status_soa(self):
        for invoice in self:
            invoice.status_soa = 'not_paid'
            soa_api = self.env['soa.integration.api'].search([],limit=1)
            if soa_api:
                if invoice.cod_soa != 0:
                    headers = {'Content-Type': 'application/json','client-id':'1','Authorization':soa_api.token}
                    url = soa_api.url_invoice+str(invoice.cod_soa)+'/'
                    if invoice.payment_state == 'paid' or invoice.payment_state == 'in_payment':
                        #IvStatus =5 es pagado, 3 es NO PAGADO, 4 es en proceso de pago
                        data = {'IvStatus':5}
                        response = requests.put(url, data=json.dumps(data),headers=headers)
                        invoice.status_soa = 'paid'
                    elif invoice.payment_state == 'not_paid':
                        data = {'IvStatus':3}
                        response = requests.put(url, data=json.dumps(data),headers=headers)
                        invoice.status_soa = 'not_paid'
        
                    if response.status_code == 200:
                        msg = response.json()['detail']
                        notification = {
                                   'type': 'ir.actions.client',
                                   'tag': 'display_notification',
                                   'params': {
                                       'title': _('Success'),
                                       'type': 'success',
                                       'message': msg,
                                       'sticky': True,
                                   }
                                }
                        return notification
                    else:
                        raise UserError(_("!Algo malo sucedio!  " + response.reason))
                    
                    
            else:
                raise UserError(_("Please configure SOA API!"))
        
            

      

    

class AccountMoveLine(models.Model):
    _inherit = ["account.move.line"]


    plan_id = fields.Many2one(comodel_name="product.planes",string="Plan")

    @api.model
    def create(self,vals):
        line = super(AccountMoveLine,self).create(vals)
        if line.plan_id:
            analytic = self.env['account.analytic.account'].search([('product_plan_id','=',line.plan_id.id)],limit=1)
            if analytic:
                if line.account_id.user_type_id.property_analytic_policy != 'never':
                    line.analytic_account_id = analytic.id

        return line

    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        for line in self:
            analytic = self.env['account.analytic.account'].search([('product_plan_id','=',line.plan_id.id)],limit=1)
            if analytic:
                line.analytic_account_id = analytic.id