from odoo import models, fields, api
from odoo.exceptions import UserError, Warning, ValidationError
import pytz


class Popupwarn(models.TransientModel):
    _name = "invoice_event_wizard"
    _description = "New invoice event wizard"

    invoice_event_id = fields.Many2one(comodel_name='invoice_event', string='Invoice Event')
    event_begin_date = fields.Datetime(string='Event Begin date')
    event_end_date = fields.Datetime(string='Event End date')

    def create_event(self):
        user_tz = pytz.timezone(self.env.context.get('tz' or self.env.user.tz))
        begin_date = pytz.utc.localize(self.event_begin_date).astimezone(user_tz).strftime("%Y-%m-%d %H:%M:%S")
        end_date = pytz.utc.localize(self.event_end_date).astimezone(user_tz).strftime("%Y-%m-%d %H:%M:%S")
        format_begin_date = self.env['account.move'].parse_date(pytz.utc.localize(self.event_begin_date).astimezone(user_tz))
        format_end_date = self.env['account.move'].parse_date(pytz.utc.localize(self.event_end_date).astimezone(user_tz))
        new_incident = {
                        "invoice_event_id": int(self.invoice_event_id.code),
                        "description": self.invoice_event_id.description,
                        "begin_date": format_begin_date,
                        "end_date": format_end_date,
                        "selling_point_id": (self.env['account.move'].getBranchOffice()[2]).id,
                        "incident_status_id": 1,
                        "sin_code": "",
                        "cufd_log_id": self.env['account.move'].get_CUFD_by_date(self.event_begin_date).id
                        }
        self.env['invoice_incident'].create(new_incident)

    def send_package(self):
        cert_status = int(self.env['bo_edi_params'].search( ## Variable de certificacion para cambio de estado Online/Offline
            [('name', '=', 'CERTSTATUS')]).value)
        
        # if not cert_status:
        #     raise Warning("You are currently in Offline mode, cannot send package yet")
        # else:
        if int(self.invoice_event_id.code) >= 4:
            if self.event_begin_date and self.event_end_date:
                self.create_event()
                res_send_package = self.env['account.move'].check_conectivity(True)
                if res_send_package:
                    raise Warning('Package sent to SIN succesfully!')    
            else:
                raise Warning('Fill in date fields please')    
        else:
            raise Warning('Manual invoices aren''t available for the current event, please change')