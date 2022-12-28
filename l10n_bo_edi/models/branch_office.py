from odoo import fields, models


class BranchOffice(models.Model):
    _name = 'branch_office'
    _description = 'branch_office'
    _rec_name = 'description' ## Para cambiar el texto a desplegar en front


    id_branch_office = fields.Integer(
        string='Branch Office Code', required=True)

    description = fields.Text(string='Description', required=True)

    address = fields.Text(string='Address', required=False)

    selling_point_ids = fields.One2many(
        'selling_point', 'branch_office_id', string='Selling Points')

    user_ids = fields.One2many(
        'res.users', 'l10n_bo_branch_office_id', string='Users')

    active = fields.Boolean(
        'Active', help='Allows you to hide the branch office without removing it.', default=True)
