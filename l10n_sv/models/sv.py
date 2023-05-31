# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class GiroNegocio(models.Model):
    _name = 'sv.giro_negocio'

    name = fields.Char("Nombre", required=True)
