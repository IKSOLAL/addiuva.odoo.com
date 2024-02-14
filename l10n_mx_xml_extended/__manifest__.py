##############################################################################
#
#    Copyright (C) 2021  Ikatech  (https://ikatechsolutions.com/)
#    All Rights Reserved.
#
##############################################################################

{
    'name': 'Account Move Assignment',
    'version': '15.0.0.0.0',
    'category': 'account',
    'summary': "Add field assignment to account move line",
    'author': "Ikatech",
    'website': 'https://ikatechsolutions.com/',
    'license': 'AGPL-3',
    'depends': [
        'account',
        ],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'odoo-license': 'EE',

}
