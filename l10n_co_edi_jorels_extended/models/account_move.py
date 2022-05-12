# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    flag_colombia = fields.Boolean(string="Colombia", compute="_compute_flag_colombia")

    @api.depends('partner_id')
    def _compute_flag_colombia(self):
        for r in self:
            for c in self.env.companies:
                if c.country_id.name == 'Colombia':
                    r.flag_colombia = True
                else:
                    r.flag_colombia = False


class ResPartner(models.Model):
    _inherit = 'res.partner'

    flag_colombia = fields.Boolean(string="Colombia", compute="_compute_flag_colombia")

    @api.depends('country_id')
    def _compute_flag_colombia(self):
        for r in self:
            for c in self.env.companies:
                if c.country_id.name == 'Colombia':
                    r.flag_colombia = True
                else:
                    r.flag_colombia = False


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    flag_colombia = fields.Boolean(string="Colombia", compute="_compute_flag_colombia")

    @api.depends('date_mode')
    def _compute_flag_colombia(self):
        for r in self:
            for c in self.env.companies:
                if c.country_id.name == 'Colombia':
                    r.flag_colombia = True
                else:
                    r.flag_colombia = False