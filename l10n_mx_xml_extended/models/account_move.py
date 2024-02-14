# -*- coding: utf-8 -*-
from odoo import models, fields,api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    l10n_mx_xml_poliza_uuid = fields.Char(string="UUID")

    @api.onchange('l10n_mx_edi_cfdi_uuid')
    def onchange_l10n_mx_xml_poliza_uuid(self):
        for move in self:
            move.l10n_mx_xml_poliza_uuid = move.l10n_mx_edi_cfdi_uuid

