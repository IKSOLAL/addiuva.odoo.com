# © 2014-2016 Acsone (http://acsone.eu)
# © 2016 Akretion (http://www.akretion.com/)
# @author Stéphane Bidoul <stephane.bidoul@acsone.eu>
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    property_partner_policy = fields.Selection(
        selection=[
            ("optional", "Optional"),
            ("always", "Always"),
            ("never", "Never")],
        string="Policy for Partner Field",
        default="optional",
        company_dependent=True,
        help="Set the policy for the partner field : if you select "
        "'Optional', the accountant is free to put a partner "
        "on an account move line with this type of account ; "
        "if you select 'Always', the accountant will get an error "
        "message if there is no partner ; if you select 'Never', "
        "the accountant will get an error message if a partner "
        "is present.",
    )
    account_journal_ids = fields.Many2many("account.journal", string="Excepto los diarios",
                                           help="Se tomara como primera evaluacion el diario y despues la excepcion de cuentas "
                                                "como nivel 2 de evaluacion")

class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        self.mapped("line_ids")._check_partner_required()
        return res


class AccountAccount(models.Model):
    _inherit = "account.account"

    def get_partner_policy(self):
        """ Extension point to obtain analytic policy for an account """
        self.ensure_one()
        return self.user_type_id.with_company(
            self.company_id.id
        ).property_partner_policy



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _check_partner_required_msg(self):
        prec = self.env.user.company_id.currency_id.rounding
        for line in self:
            if self.move_id.journal_id.id in self.account_id.user_type_id.account_journal_ids.ids:
                return None

            if float_is_zero(line.debit, precision_rounding=prec) and float_is_zero(
                line.credit, precision_rounding=prec
            ):
                continue
            policy = line.account_id.get_partner_policy()
            if policy == "always" and not line.partner_id:
                return _(
                    "Partner policy is set to 'Always' with account '%s' but "
                    "the partner is missing in the account move line with "
                    "label '%s'."
                ) % (line.account_id.name_get()[0][1], line.name)
            elif policy == "never" and line.partner_id:
                return _(
                    "Partner policy is set to 'Never' with account '%s' but "
                    "the account move line with label '%s' has a partner "
                    "'%s'."
                ) % (line.account_id.name_get()[0][1], line.name, line.partner_id.name)

    #@api.constrains("partner_id", "account_id", "debit", "credit")
    def _check_partner_required(self):
        for line in self:
            message = line._check_partner_required_msg()
            if message:
                raise ValidationError(message)
