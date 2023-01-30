from odoo import models, fields, api

class Popupwarn(models.TransientModel):
    _name = "popup_warn_wizard"
    _description = "Simple popup warning"
    
    def to_continue(self):
        self.env['account.move'].check_conectivity()