from odoo import fields, models


class Messages_service(models.Model):
    _name = 'messages_service'
    _description = 'BO EDI Messages Service'

    code = fields.Char('code')

    description = fields.Char('Message')
