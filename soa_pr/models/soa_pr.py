# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SoaPrExtended(models.Model):
    _name = 'soa.pr'
    _description = 'Model that will store the data'
    _rec_name = 'id'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente', help='Selecciona el cliente')
    account_id_soa = fields.Integer(string='Account ID SOA', help='Escribe el ID SOA')
    client_id_soa = fields.Integer(string='Client ID SOA', help='Escribe el Client ID SOA')
    plan_soa = fields.Many2one(comodel_name='product.planes', string='Plan', help='Selecciona el plan')
    plan_id_soa = fields.Char(string="PLAN ID SOA")

    @api.onchange('plan_soa')
    def _onchange_plan_soa(self):
        if self.plan_soa:
            self.plan_id_soa = self.plan_soa.cod_soa
        else:
            self.plan_id_soa = False

    plan_id_odoo = fields.Char(string="PLAN ID ODOO")

    @api.onchange('plan_soa')
    def _onchange_plan_id_odoo(self):
        if self.plan_soa:
            self.plan_id_odoo = self.plan_soa.id
        else:
            self.plan_id_odoo = False

    
    plan_name = fields.Char(string='Nombre del plan', help='Escribe el nombre del plan')
    serv_description = fields.Char(string='Descripcion del servicio', help='Escribe la descripcion del servicio')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Compañía',
         default=lambda self: self.env['res.company'].browse(self.env['res.company']._company_default_get('soa_pr')),
        help='Compañía asociada al usuario logueado'
    )
    