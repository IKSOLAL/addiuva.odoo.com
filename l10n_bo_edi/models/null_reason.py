from odoo import fields, models


class Null_reason(models.Model):
    _name = 'null_reason'
    _description = 'BO EDI Null Reason'

    code = fields.Char('code')

    description = fields.Char('Message')
