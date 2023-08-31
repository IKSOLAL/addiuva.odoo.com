# -*- coding: utf-8 -*-

from odoo import models, fields, api

class l10n_mx_reports_extend(models.AbstractModel):
    _inherit = 'l10n_mx.coa.report'


    def _get_coa_dict(self, options):
        res = super(l10n_mx_reports_extend, self)._get_coa_dict(options)
        for account in res['accounts']:
            code = account['code'].split('.')
            if len(code) > 1: 
                code = code[0]
            else:
                 code = account['code']
            account['subaccount'] = code
        accounts_list = self.env['account.account'].search([('deprecated','=',False),('company_id','=', self.env.company.id)])
        for account in accounts_list:
            if account.tag_ids:
                sat_group_code = account.tag_ids[0].name.split(' ')
                res['accounts'].append({
                    'code': sat_group_code[0],
                    'number': account.code,
                    'name':  account.name,
                    'level': '3',
                    'subaccount': sat_group_code[0],
                    'nature': account.tag_ids[0].nature,
                })
        return res
