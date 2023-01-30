# -*- coding: utf-8 -*-

from odoo import models, fields, api


class account_move_features(models.Model):
    _inherit = 'account.move'

    entry_tax_bolivia = fields.Many2one('account.move')

    def create_entry_taxes(self):
        # if self.company_id.country_id.name == "Bolivia":
        if self.move_type == "out_invoice":
            #create entry with accounts number 24020004 - Debit | 62066006 - Credit, in all customer invoices in Bolivia Country
            move_id = self.env['account.move'].create({
                'date': self.date,
                'move_type': "entry",
                'journal_id': 422, #-> ID Journal Impuestos IT
                'partner_id': self.partner_id.id,
                'ref': "{}: {}".format(self.name, self.partner_id.name),
            })
            self.env['account.move.line'].create([{
                'ref': "",
                'account_id': 26907, # -> ID from account 62066006
                'name': "{}: {}".format(self.name, self.partner_id.name),
                'debit': self.amount_untaxed * 0.03,
                'credit': 0,
                'partner_id': self.partner_id.id,
                'move_id': move_id.id
            },{
                'ref': "",
                'account_id': 26699, # -> ID from account 24020004
                'name': "{}: {}".format(self.name, self.partner_id.name),
                'debit': 0,
                'credit': self.amount_untaxed * 0.03,
                'partner_id': self.partner_id.id,
                'move_id': move_id.id
            }])
            move_id.action_post()
            self.entry_tax_bolivia = move_id