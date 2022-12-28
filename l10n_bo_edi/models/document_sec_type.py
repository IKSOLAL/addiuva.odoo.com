from odoo import fields, models


class Document_sec_type(models.Model):
    _name = 'document_sec_type'
    _description = 'BO EDI Native Country'

    code = fields.Char('code')

    description = fields.Char('description')
