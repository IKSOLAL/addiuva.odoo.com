# -*- coding: utf-8 -*-
from odoo import models, fields,api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    eaccount_complements_ids = fields.One2many('eaccount.complements','move_line_id',
                                               string="UUID")
    enable_uuid_btn = fields.Boolean(related="account_id.include_uuid_edi")
    count_uuid = fields.Boolean(compute="_compute_count_uuid")

    @api.depends('eaccount_complements_ids')
    def _compute_count_uuid(self):
        self.count_uuid = len(self.eaccount_complements_ids)
        print(self.count_uuid)

    def open_wizard_uuid(self):
        view_id = self.env.ref('l10n_mx_xml_extended.view_eaccount_complements_form').id
        return {
            'name': ('Datos de comprobantes'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view_id],
            'res_model': 'account.move.line',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

