from odoo import api, fields, models


# Display amount in words in Sale order
class HrExpense(models.Model):
    _inherit = 'hr.expense'

    #accounting_date = fields.Date(string="Accounting Date", related='sheet_id.accounting_date', store=True,
    #                              groups='account.group_account_invoice,account.group_account_readonly')
    accounting_date = fields.Date(string="Accounting Date", compute="_compute_accounting_date",
                                  inverse="_inverse_accounting_date"
                                  ,groups='account.group_account_invoice,account.group_account_readonly')
    @api.depends('sheet_id.accounting_date')
    def _compute_accounting_date(self):
        for r in self:
            r.accounting_date = r.sheet_id.accounting_date

    def _inverse_accounting_date(self):
        for r in self:
            r.sheet_id.accounting_date = r.accounting_date
    def _get_default_expense_sheet_values(self):
        res = super(HrExpense,self)._get_default_expense_sheet_values()
        res['default_accounting_date'] = self.accounting_date
        return res

