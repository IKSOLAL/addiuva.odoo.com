# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountFiscalyearUpdateRecords(models.TransientModel):
    """
    Added Fiscal Year in Exsting Records
    """
    _name = "account.fiscalyear.update.records"
    _description = "Fiscalyear Update Exsting Records"

    def data_update_records(self):
        """
        This function close account fiscalyear
        """
        account_move_obj = self.env['account.move']

        account_invoice_ids = account_move_obj.search([])
        if account_invoice_ids:
            for invoice in account_invoice_ids:
                if invoice.invoice_date:
                    today = invoice.invoice_date
                    period_id = self.env['account.period'].search([('date_start','<=',today), ('date_stop','>=',today)], limit=1)
                    if period_id:
                        self._cr.execute('update account_move set period_id=%s,fiscalyear_id=%s where id=%s', (period_id.id, period_id.fiscalyear_id.id, invoice.id))
                        self._cr.execute('update account_move_line set period_id=%s,fiscalyear_id=%s where move_id=%s', (period_id.id, period_id.fiscalyear_id.id, invoice.id))
                    else:
                        raise UserError(_('The periods does not exist, Please create Fiscal Year & Periods For Date (%s)!') % (today))
        account_move_ids = account_move_obj.search([])
        if account_move_ids:
            for move in account_move_ids:
                move_date = move.date
                if move_date:
                    period_id = self.env['account.period'].search([('date_start','<=',move_date), ('date_stop','>=',move_date)], limit=1)
                    if period_id:
                        self._cr.execute('update account_move set period_id=%s,fiscalyear_id=%s where id=%s', (period_id.id, period_id.fiscalyear_id.id, move.id))
                        self._cr.execute('update account_move_line set period_id=%s,fiscalyear_id=%s where move_id=%s', (period_id.id, period_id.fiscalyear_id.id, move.id))
                    else:
                        raise UserError(_('The periods does not exist, Please create Fiscal Year & Periods For Date (%s)!') % (move_date))

        return {'type': 'ir.actions.act_window_close'}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
