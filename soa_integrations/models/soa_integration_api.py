# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError
import requests, json


class SoaIntegrationApi(models.Model):
    _name = 'soa.integration.api'

    username = fields.Char(string="Username")
    password = fields.Char(string="Password")
    client_id = fields.Char(string="Clien-ID")
    token = fields.Char(string="Token")
    url_login = fields.Char(string="Url Login")
    url_invoice = fields.Char(string="Url Factura")

    #company_id = fields.Many2one(comodel_name='res.company', string="Empresa",
    #                             default=lambda self:    self.env['res.company'].browse(self.env['res.company']._company_default_get('ik_integrations_group')))
    company_id = fields.Many2one(comodel_name='res.company', string="Empresa")
    soa_enabled = fields.Boolean(string="Activar SOA")



    def get_token(self):
        r = requests.post(self.url_login, json={
            "username": self.username,
            "password": self.password,
            })
        if r.status_code == 200:
           jsondata = r.json()
           self.token = jsondata['access_token']
        else:
            raise UserError('API is not available')
           
        





