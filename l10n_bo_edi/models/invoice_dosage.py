from odoo import fields, models


class Invoice_dosage(models.Model):
    _name = 'invoice_dosage'
    _description = 'BO SIN invoice dosage'
    _rec_name = 'code' ## Para cambiar el texto a desplegar en front

    code = fields.Text('Code')

    auth_number = fields.Text('Authorization Number')

    end_date = fields.Date('Dosage Deadline')

    selling_point_id = fields.Many2one('selling_point', string='Selling Point')

    invoice_number = fields.Integer('Invoice Number')

    key = fields.Text('Dosage Key')

    invoice_caption = fields.Text('Invoice Caption')

    activity_id = fields.Many2one('l10n_bo.company.activities', string='Activity Code')
    
