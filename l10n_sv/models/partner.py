# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class Partner(models.Model):
    _inherit = "res.partner"

    pequenio_contribuyente = fields.Boolean(string="Pequeño Contribuyente")
    numero_registro = fields.Char('Registro')
    giro_negocio_id = fields.Many2one('sv.giro_negocio', 'Giro')
    consumidor_final = fields.Boolean('Consumidor final')
    dui = fields.Char('DUI')
