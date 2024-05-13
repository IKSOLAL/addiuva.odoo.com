# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.move.line'

    def open_wizard(self):
        return {
            'name': 'Actualizar Apuntes de Diario',
            'domain': '',
            'view_type': 'form',
            'res_model': 'account.line.massediting',
            'view_id': False,
            'views': [(self.env.ref('account_move_line_edit.account_line_massediting_wizard').id, 'form')],
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'active_ids': self.env.context.get('active_ids', [])},
        }


class AccountMoveLineMassediting(models.TransientModel):
    _name = 'account.line.massediting'

    account_analytic_id = fields.Many2one('account.analytic.account')
    delete_aa = fields.Boolean()
    analytic_tags_id = fields.Many2many('account.analytic.tag')
    delete_at = fields.Boolean()
    tag = fields.Char()
    delete_tag = fields.Boolean()
    account_id = fields.Many2one('account.account')
    delete_cc = fields.Boolean()
    partner_id = fields.Many2one('res.partner')
    delete_partner = fields.Boolean()

    def update_records_edit(self):
        move_lines_ids = self.env.context.get('active_ids', [])
        account_move_lines = self.env['account.move.line'].browse(
            move_lines_ids)
        for line in account_move_lines:
            if self.account_id or self.delete_cc:
                cc = False if self.delete_cc else self.account_id.id
                line.write({'account_id': cc})
                self.env['account.analytic.line'].search([('move_id', '=', line.id)]).write({
                    'general_account_id': cc})
            if self.account_analytic_id or self.delete_aa:
                aa = False if self.delete_aa else self.account_analytic_id.id
                analytic_move = self.env['account.analytic.line'].search([('move_id', '=', line.id)])
                line.write(
                    {'analytic_account_id': aa})
                if aa == False:
                    analytic_move.unlink()
                else:
                    self.env['account.analytic.line'].search([('move_id', '=', line.id)]).write({
                        'account_id': aa})
            if self.analytic_tags_id or self.delete_at:
                ats = False if self.delete_at else self.analytic_tags_id.ids
                line.write({'analytic_tag_ids': ats})
                self.env['account.analytic.line'].search([('move_id', '=', line.id)]).write({
                    'tag_ids': ats})
            if self.partner_id or self.delete_partner:
                partner = False if self.delete_partner else self.partner_id.id
                line.write({'partner_id': partner})
                self.env['account.analytic.line'].search([('move_id', '=', line.id)]).write({
                    'partner_id': partner})
            if self.tag or self.delete_tag:
                tag = "" if self.delete_tag else self.tag
                line.write({'name': tag})
                self.env['account.analytic.line'].search(
                    [('move_id', '=', line.id)]).write({'name': tag})
