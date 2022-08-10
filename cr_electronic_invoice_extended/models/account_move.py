# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    flag_cr = fields.Boolean(string="Costa Rica", compute="_compute_flag_cr")

    @api.depends('partner_id')
    def _compute_flag_cr(self):
        for r in self:
            for c in self.env.companies:
                if c.country_id.name == 'Costa Rica':
                    r.flag_cr = True
                else:
                    r.flag_cr = False


class ResPartner(models.Model):
    _inherit = 'res.partner'

    flag_cr = fields.Boolean(string="Costa Rica", compute="_compute_flag_cr")

    @api.depends('country_id')
    def _compute_flag_cr(self):
        for r in self:
            for c in self.env.companies:
                if c.country_id.name == 'Costa Rica':
                    r.flag_cr = True
                else:
                    r.flag_cr = False


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    flag_cr = fields.Boolean(string="Costa Rica", compute="_compute_flag_cr")

    @api.depends('date_mode')
    def _compute_flag_cr(self):
        for r in self:
            for c in self.env.companies:
                if c.country_id.name == 'Costa Rica':
                    r.flag_cr = True
                else:
                    r.flag_cr = False