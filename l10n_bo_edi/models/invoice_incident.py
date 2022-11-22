from odoo import fields, models


class Invoice_incident(models.Model):
    _name = 'invoice_incident'
    _description = 'BO EDI Invoice Incident'
    _rec_name = 'description' ## Para cambiar el texto a desplegar en front


    invoice_event_id = fields.Many2one(comodel_name='invoice_event', string='Invoice Event')
    
    description = fields.Char('Description')

    begin_date = fields.Datetime(string='Begin Date')
    
    end_date = fields.Datetime(string='End Date')

    selling_point_id = fields.Many2one(comodel_name='selling_point', string='Selling Point')

    # incident_status_id = fields.Many2one(comodel_name='incident_status', string='Incident Status')
    ##//!! error al asignar modelo init "from partially initialized module"
    
    incident_status_id = fields.Integer(string='Incident Status')
    
    sin_code = fields.Char(string='SIN code')

    cufd_log_id = fields.Many2one(comodel_name='cufd_log', string='CUFD related')
    
        

    
    
