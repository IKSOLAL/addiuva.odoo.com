# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

msg_alert = "No se cuenta con permisos para realizar esta operación. Favor de contactar con el administrador."

class ResPartnerAccess(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create(self, vals):
        res = super(ResPartnerAccess, self).create(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(ResPartnerAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
class AccountAccountAccess(models.Model):
    _inherit = 'account.account'
    
    @api.model
    def create(self, vals_list):
        res = super(AccountAccountAccess, self).create(vals_list)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(AccountAccountAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
     
class AccountAnalyticAccountAccess(models.Model):
    _inherit = 'account.analytic.account'
    
    @api.model
    def create(self, vals_list):
        res = super(AccountAnalyticAccountAccess, self).create(vals_list)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(AccountAnalyticAccountAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
class AccountAnalyticTagAccess(models.Model):
    _inherit = 'account.analytic.tag'
    
    @api.model
    def create(self, vals_list):
        res = super(AccountAnalyticTagAccess, self).create(vals_list)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(AccountAnalyticTagAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
class AccountTaxAccess(models.Model):
    _inherit = 'account.tax'
    
    @api.model
    def create(self, vals_list):
        res = super(AccountTaxAccess, self).create(vals_list)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(AccountTaxAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res

class AccountJournalAccess(models.Model):
    _inherit = 'account.journal'
    
    @api.model
    def create(self, vals_list):
        res = super(AccountJournalAccess, self).create(vals_list)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(AccountJournalAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
class ProductTemplateAccess(models.Model):
    _inherit = 'product.template'
    
    @api.model
    def create(self, vals_list):
        res = super(ProductTemplateAccess, self).create(vals_list)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(ProductTemplateAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
class ProductCategoryAccess(models.Model):
    _inherit = 'product.category'
    
    @api.model
    def create(self, vals_list):
        res = super(ProductCategoryAccess, self).create(vals_list)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res
    
    def write(self, vals):
        res = super(ProductCategoryAccess, self).write(vals)
        if not self.env.user.has_group('access_rights_extend.ikatech_permissions'):
            raise exceptions.ValidationError(msg_alert)
        return res