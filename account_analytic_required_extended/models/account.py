from odoo import fields, models


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    account_account_ids = fields.Many2many("account.account", string="Excepto las cuentas")


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _check_analytic_required_msg(self):
        res = super(AccountMoveLine, self)._check_analytic_required_msg()
        if res:
            if self.account_id.id in self.account_id.user_type_id.account_account_ids.ids:
                return None
            else:
                res
        return res
