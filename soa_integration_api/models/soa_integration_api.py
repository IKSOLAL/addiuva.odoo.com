# -*- coding: utf-8 -*-

from odoo import models, fields


class SoaIntegrationApi(models.Model):
    _name = 'soa.integration.api'

    username = fields.Char(string="Username")
    password = fields.Char(string="Password")
    client_id = fields.Char(string="Clien-ID")
    authorization = fields.Char(string="Authorization")





