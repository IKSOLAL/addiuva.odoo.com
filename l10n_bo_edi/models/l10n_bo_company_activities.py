from odoo import api, fields, models
from odoo.osv import expression


class CompanyActivities(models.Model):
    _description = 'SII Company Economical Activities'
    _name = 'l10n_bo.company.activities'

    code = fields.Char('Activity Code', required=True)
    name = fields.Char('Complete Name', required=True)
    # tax_category = fields.Selection([
    #     ('1', '1'),
    #     ('2', '2'),
    #     ('nd', 'ND')
    # ], 'TAX Category', default='1', help='If your company is 2nd category tax payer type, you should use activity '
    #                                      'codes of type 2, otherwise they should be type 1. '
    #                                      'If your activity is affected by vat tax depending on other situations, '
    #                                      'SII uses type ND. In every cases the tax category is defined by the CIIU4.CL '
    #                                      'nomenclature adopted by SII, and you should only add new activities in case '
    #                                      'they are added in the future.')
    type = fields.Selection([
        ('S', 'S'),
        ('P', 'P')
    ], string='')

    sin_item_ids = fields.One2many(
        'sin_items', 'activity_code', string='SIN Items')

    active = fields.Boolean(
        'Active', help='Allows you to hide the activity without removing it.', default=True)

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = '(%s) %s' % (record.code, record.name)
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not(name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
