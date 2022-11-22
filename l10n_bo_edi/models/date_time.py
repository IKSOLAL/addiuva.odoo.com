from odoo import fields, models


class Date_time(models.Model):
    _name = 'boedi_date_time'
    _description = 'Date and time data sync with SIN'

    date_time = fields.Text(string='Date and Time')

    active = fields.Boolean(
        'Active', help='Allows you to hide the date_time without removing it.', default=True)
