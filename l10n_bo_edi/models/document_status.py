from odoo import fields, models, api


class DocumentStatus(models.Model):
    _name = 'document_status'
    _description = 'SIN document status'

    code = fields.Integer('code')

    description = fields.Text('description')

    active = fields.Boolean(
        'Active', help='Allows you to hide the document status without removing it.', default=True)
