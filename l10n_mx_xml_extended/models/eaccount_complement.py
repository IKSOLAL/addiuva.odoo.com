# -*- coding: utf-8 -*-
from odoo import models, fields,api
from odoo.exceptions import UserError


class EAccountComplements(models.Model):
    _name = 'eaccount.complements'
    _description = 'UUID que complementan informacion para los XML de POLIZAS'

    uuid = fields.Char(string="UUID", help="UUID del CFDI")
    date = fields.Date(string="Fecha")
    rfc_receiver = fields.Char(string="RFC Receptor")
    rfc_issuer = fields.Char(string="RFC Emisor")
    amount = fields.Float(string="Monto")
    folio = fields.Char(string="Folio")
    serie = fields.Char(string="Serie")
    move_line_id = fields.Many2one(comodel_name="account.move.line",string="Move Line Related")

    @api.model
    def create(self,vals_list):
        line_ids = self.env['account.move'].search([('id', '=', self.move_line_id.move_id.id)]).line_ids
        debits = sum(line_ids.mapped('debit'))
        res = super(EAccountComplements,self).create(vals_list)
        uuid_ids = self.env['eaccount.complements'].search([('move_line_id', '=', self.move_line_id.id)])
        amounts = sum(uuid_ids.mapped('amount'))
        if amounts > debits:
            raise UserError('La sumatoria de los montos totales es mayor a los cargos')
        return res


    def write(self, vals_list):
        line_ids = self.env['account.move'].search([('id', '=', self.move_line_id.move_id.id)]).line_ids
        debits = sum(line_ids.mapped('debit'))
        res = super(EAccountComplements, self).write(vals_list)

        uuid_ids = self.env['eaccount.complements'].search([('move_line_id','=',self.move_line_id.id)])
        amounts = sum(uuid_ids.mapped('amount'))
        if amounts > debits:
            raise UserError('La sumatoria de los montos totales es mayor a los cargos')
        return res








