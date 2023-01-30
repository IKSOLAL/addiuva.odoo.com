from odoo import fields, models, api


class SinToken(models.Model):
    _name = 'sin_token'
    _description = 'Tokens provided by SIN'
    _rec_name = 'end_date' ## Para cambiar el texto a desplegar en front

    begin_date = fields.Date(string='Begin Date')

    end_date = fields.Date(string='End Date')

    token = fields.Text(string='Token')

    notif_days = fields.Integer(string='Notification Days')

    
    