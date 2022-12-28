from odoo import fields, models


class Invoice_events(models.Model):
    _name = 'invoice_event'
    _description = 'BO EDI Invoice Events'
    _rec_name = 'description' ## Para cambiar el texto a desplegar en front

    code = fields.Char('code')

    description = fields.Char('Message')
