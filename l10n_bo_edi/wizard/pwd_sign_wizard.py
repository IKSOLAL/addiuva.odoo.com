from odoo import models, fields, api
from odoo.exceptions import UserError, Warning, ValidationError

class Pwdsignwizard(models.TransientModel):
    _name = "pwd_sign_wizard"
    _description = "Pwd sign wizard"
    
    pwd_sign = fields.Char(string='Ingrese su PIN')

    pwd_sign_confirm = fields.Char(string='Confirme su PIN')

    def save_pwd(self):
        if self.pwd_sign != self.pwd_sign_confirm:
            raise Warning("Las contraseñas no coinciden, favor de probar nuevamente")
        else:
            self.env['bo_edi_params'].create({
                    "param_code" : 24,
                    "name" : "PWD_DIG_SIGN",
                    "value": self.pwd_sign_confirm
                })

    