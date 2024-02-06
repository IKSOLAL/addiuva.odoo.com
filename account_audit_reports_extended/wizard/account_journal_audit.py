# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import fields, models, api


class AccountPrintJournal(models.TransientModel):
    _inherit = "account.print.journal"

    def _print_report(self, data):
        if self._context.get('excel_report'):
            data = self.pre_print_report(data)
            data['form'].update({'sort_selection': self.sort_selection})
            return self.env.ref('account_audit_reports_extended.action_report_journal_excel').report_action(
                self, data=data)
        else:
            return super(AccountPrintJournal, self)._print_report(data)
