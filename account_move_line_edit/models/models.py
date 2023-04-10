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
            'type':'ir.actions.act_window',
            'target': 'new',
            'context': {'active_ids': self.env.context.get('active_ids', [])},
        }


class AccountMoveLineMassediting(models.TransientModel):
    _name =  'account.line.massediting'

    account_analytic_id = fields.Many2one('account.analytic.account')
    analytic_tags_id = fields.Many2many('account.analytic.tag')
    tag = fields.Char()
    account_id = fields.Many2one('account.account')
    partner_id = fields.Many2one('res.partner')

    def update_records_edit(self):
        move_lines_ids = self.env.context.get('active_ids', [])
        account_move_lines=self.env['account.move.line'].browse(move_lines_ids)
        for line in account_move_lines:
            if self.account_analytic_id:
                line.write({'analytic_account_id': self.account_analytic_id.id})
                self.env['account.analytic.line'].search([('move_id','=', line.id)]).write({'account_id':self.account_analytic_id.id})
            if self.analytic_tags_id:
                line.write({'analytic_tag_ids': self.analytic_tags_id.ids})
                self.env['account.analytic.line'].search([('move_id','=', line.id)]).write({'tag_ids':self.analytic_tags_id.ids})
            if self.account_id:
                line.write({'account_id': self.account_id.id})
                self.env['account.analytic.line'].search([('move_id','=', line.id)]).write({'general_account_id':self.account_id.id})
            if self.partner_id:
                line.write({'partner_id': self.partner_id.id})
                self.env['account.analytic.line'].search([('move_id','=', line.id)]).write({'partner_id':self.partner_id.id})
            if self.tag:
                line.write({'name': self.tag})
                self.env['account.analytic.line'].search([('move_id','=', line.id)]).write({'name':self.tag})