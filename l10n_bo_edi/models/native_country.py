from odoo import fields, models


class Native_country(models.Model):
    _name = 'native_country'
    _description = 'BO EDI Native Country'

    code = fields.Char('code')

    description = fields.Char('description')
