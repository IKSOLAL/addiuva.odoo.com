# -*- coding: utf-8 -*-

from odoo import models, fields, api


class crm_extend(models.Model):
    _inherit = 'crm.lead'

    industries = fields.Many2one('crm.industries', string="Industrias")
    services = fields.Many2one('crm.services', string="Servicios")
    inactive = fields.Boolean(string="Inactivo", default=False)
    stage_name = fields.Char(related='stage_id.name')


    @api.onchange("stage_id")
    def onchange_stage(self):
        for rec in self:
            if rec.stage_id.name == "Suspecto":
                rec.probability = 0
            if rec.stage_id.name == "Prospecto":
                rec.probability = 0
            if rec.stage_id.name == "Cita Inicial":
                rec.probability = 10
            if rec.stage_id.name == "Diagnostico":
                rec.probability = 30
            if rec.stage_id.name == "Demostración":
                rec.probability = 50
            if rec.stage_id.name == "Negociación":
                rec.probability = 70
            if rec.stage_id.name == "Cierre":
                rec.probability = 90

    def mark_as_inactive(self):
        self.inactive = True

    def mark_as_active(self):
        self.inactive = False

class CRMIndustries(models.Model):
    _name = 'crm.industries'
    _rec_name = 'name'

    name = fields.Char(string="Industria")


class CRMServices(models.Model):
    _name = 'crm.services'
    _rec_name = 'name'

    name = fields.Char(string="Servicios")