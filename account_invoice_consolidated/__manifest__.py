# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Invoice Consolidated',
    'version': '12.0.1.1.0',
    'summary': 'Consolidate your invoices across companies',
    'author': 'Open Source Integrators, '
              'Serpent Consulting Services Pvt. Ltd., '
              'Odoo Community Association (OCA)',
    'category': 'Invoicing Management',
    'website': 'https://github.com/OCA/account-consolidation',
    'license': 'AGPL-3',
    'depends': [
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_view.xml',
    ],
    'application': True,
    'development_status': 'Beta',
    'maintainers': [
        'max3903',
        'swapnesh-serpentcs',
    ]
}
