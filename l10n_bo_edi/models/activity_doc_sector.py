from odoo import fields, models


class Activity_doc_sector(models.Model):
    _name = 'activity_doc_sector'
    _description = 'Relation Model between Sectors and Activities'

    activity_code = fields.Char('Activity Code')

    sector_doc_code = fields.Char('Sector Doc Code')

    sector_doc_type = fields.Char('Sector Doc type')
