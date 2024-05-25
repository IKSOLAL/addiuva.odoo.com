from odoo import _, api, exceptions, fields, models
from odoo.tools import float_is_zero
from odoo.exceptions import ValidationError


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    property_analytic_tag_policy = fields.Selection(
        selection=[
            ("optional", "Optional"),
            ("always", "Always"),
            ("never", "Never")],
        string="Policy for Analytic Tag Field",
        default="optional",
        company_dependent=True,
        help="Set the policy for the partner field : if you select "
             "'Optional', the accountant is free to put a analytic tag "
             "on an account move line with this type of account ; "
             "if you select 'Always', the accountant will get an error "
             "message if there is no analytic tag ; if you select 'Never', "
             "the accountant will get an error message if a analytic tag "
             "is present.",
    )

class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        self.mapped("line_ids")._check_analytic_tag_required()
        return res


class AccountAccount(models.Model):
    _inherit = "account.account"

    def get_analytic_tag_policy(self):
        """ Extension point to obtain analytic policy for an account """
        self.ensure_one()
        return self.user_type_id.with_company(
            self.company_id.id
        ).property_analytic_tag_policy



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _check_analytic_tag_required_msg(self):
        prec = self.env.user.company_id.currency_id.rounding
        for line in self:
            if self.move_id.journal_id.id in self.account_id.user_type_id.account_journal_ids.ids:
                return None

            if self.account_id.id in self.account_id.user_type_id.account_account_ids.ids:
                return None

            if float_is_zero(line.debit, precision_rounding=prec) and float_is_zero(
                line.credit, precision_rounding=prec
            ):
                continue
            policy = line.account_id.get_analytic_tag_policy()
            if policy == "always" and not line.analytic_tag_ids:
                return _(
                    "Analytic tag policy is set to 'Always' with account '%s' but "
                    "the analytic tag is missing in the account move line with "
                    "label '%s'."
                ) % (line.account_id.name_get()[0][1], line.name)
            elif policy == "never" and line.partner_id:
                count = 0
                tag = False
                for a in line.analytic_tag_ids:
                    if count == 0:
                        tag = a.name
                        count += 1

                return _(
                    "Analytic tag policy is set to 'Never' with account '%s' but "
                    "the account move line with label '%s' has a Analytic tag "
                    "'%s'."
                ) % (line.account_id.name_get()[0][1], line.name, tag)

    def _check_analytic_tag_required(self):
        for line in self:
            message = line._check_analytic_tag_required_msg()
            if message:
                raise ValidationError(message)
