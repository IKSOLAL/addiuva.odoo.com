from odoo import fields, models


class Invoice_caption(models.Model):
    _name = 'invoice_caption'
    _description = 'BO EDI invoice captions'

    activity_code = fields.Char('Activity Code')

    description = fields.Char('Caption')
