##############################################################################
#
#    Copyright (C) 2021  Ikatech  (https://ikatechsolutions.com/)
#    All Rights Reserved.
#
##############################################################################

{
    'name': 'XML Polizas',
    'version': '15.0.0.0.0',
    'category': 'account',
    'summary': "Replace UUID for xml",
    'author': "Ikatech",
    'website': 'https://ikatechsolutions.com/',
    'license': 'AGPL-3',
    'depends': [
        'l10n_mx_xml_polizas_edi','l10n_mx_edi',
        ],
    'data': [
        'views/account_move_view.xml',
        'views/account_account_view.xml',
        'views/eaccount_complement_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'odoo-license': 'EE',

}
