from odoo import fields, models

class BoEdiLogs(models.Model):
    _name = 'bo_edi_logs'
    _description = 'Bolivian Electronic Invoicing Logs'

    date = fields.Text(string='Emission Date')

    invoice_date = fields.Text(string='Invoice Date')

    user = fields.Text(string='User')

    inv_name = fields.Text(string='Invoice Name')

    item_val = fields.Boolean(string='Item Validation', readonly=True, default=False)

    client_val = fields.Boolean(string='Client Validation', readonly=True, default=False)

    header = fields.Boolean(string='Invoice Header', readonly=True, default=False)

    items = fields.Boolean(string='Invoice Items', readonly=True, default=False)

    emit = fields.Boolean(string='Invoice Emit', readonly=True, default=False)

    xml = fields.Boolean(string='Invoice XML', readonly=True, default=False)

    last_req = fields.Text(string='Last Request', default = 'N/A')

    last_res = fields.Text(string='Last Response', default = 'N/A')

    status = fields.Text(string='Invoice Emission Status', default = 'SIN ENVIAR')

    internal_code = fields.Integer(string='Internal Code', default = 0)
    
    active = fields.Boolean(
        'Active', help='Allows you to hide log without removing it.', default=True)