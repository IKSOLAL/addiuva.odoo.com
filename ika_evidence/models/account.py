# -*- coding: utf-8 -*-
from odoo import models, fields, api, _,exceptions
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    property_evidence_policy = fields.Selection(
        selection=[
            ("optional", "Optional"),
            ("always", "Always"),
            ("never", "Never")],
        string="Policy for Attachment File",
        default="optional",
        company_dependent=True,
        help="Set the policy for the evidence field : if you select "
        "'Optional', the accountant is free to put an attachment "
        "on an account move with this type of account ; "
        "if you select 'Always', the accountant will get an error "
        "message if there is no partner ; if you select 'Never', "
        "the accountant will get an error message if an attachment "
        "is present.",
    )

class AccountAccount(models.Model):
    _inherit = "account.account"

    def get_attachment_policy(self):
        """ Extension point to obtain analytic policy for an account """
        self.ensure_one()
        return self.user_type_id.with_company(
            self.company_id.id
        ).property_evidence_policy

class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Module to attach evidence (documents) for accounting entries'

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        self.mapped("line_ids")._check_attachment_required()
        return res

    def check_has_attachments(self):
        chatter_attachments = self.env['ir.attachment'].search([
            ('res_model', '=', 'account.move'),
            ('res_id', '=', self.id),
        ])
        if not chatter_attachments:
            return False
        else:
            return True


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _check_attachment_required_msg(self):
        for line in self:
            if self.move_id.journal_id.id in self.account_id.user_type_id.account_journal_ids.ids:
                return None

            policy = line.account_id.get_attachment_policy()
            attachment_found = self.move_id.check_has_attachments()
            if policy == "always" and not attachment_found:
                return _(
                    "Attachment policy is set to 'Always' with account '%s' but "
                    "the attachment is missing in the account move with "
                    "label '%s'."
                ) % (line.account_id.name_get()[0][1], line.name)
            elif policy == "never" and line.partner_id:
                return _(
                    "Attachment policy is set to 'Never' with account '%s' but "
                    "the account move with label '%s' has a partner "
                    "'%s'."
                ) % (line.account_id.name_get()[0][1], line.name, line.partner_id.name)

    #@api.constrains("partner_id", "account_id", "debit", "credit")
    def _check_attachment_required(self):
        for line in self:
            message = line._check_attachment_required_msg()
            if message:
                raise ValidationError(message)
