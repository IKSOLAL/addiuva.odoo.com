from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Users inherit'

    l10n_bo_is_seller = fields.Boolean(
        string='Selling Point Manager', default=False)

    l10n_bo_branch_office_id = fields.Many2one(
        'branch_office', string='Branch Office')

    l10n_bo_selling_point_id = fields.Many2one(
        'selling_point', string='Selling Point')

    internal_code = fields.Integer(string='Internal Server Code', default=0)