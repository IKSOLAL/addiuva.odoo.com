from odoo import fields, models, api


class BoEdiParams(models.Model):
    _name = 'bo_edi_params'
    _description = 'BO EDI TEST Params'

    param_code = fields.Integer(string='Param Code')

    name = fields.Text(string='Name')

    value = fields.Text(string='Value')

    active = fields.Boolean(
        'Active', help='Allows you to hide the param without removing it.', default=True)
    
    def launch_pwd_wizard(self):
        return {
                    "type": "ir.actions.act_window",
                    "res_model": "pwd_sign_wizard",
                    "view_type": "form",
                    "view_mode": "form",
                    "target": "new",
                }
    

