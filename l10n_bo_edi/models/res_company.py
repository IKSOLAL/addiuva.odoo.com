from odoo import fields, models
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_bo_dfe_service_provider = fields.Selection([
        ('SINTEST', 'SIN - Test'),
        ('SIN', 'SIN - Production')], 'DFE Service Provider',
        help='Please select your company service provider for DFE service.')

    l10n_bo_company_activity_ids = fields.Many2many('l10n_bo.company.activities', string='Activities Names',
                                                    help='Please select the SIN registered economic activities codes for the company', readonly=False)
