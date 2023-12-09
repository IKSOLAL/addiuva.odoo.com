##############################################################################
#
#    Copyright (C) 2021  Ikatech  (https://ikatechsolutions.com/)
#    All Rights Reserved.
#
##############################################################################
{
    'name': 'Ikatech Hr Expense',
    'version': '15.0.0.0.1',
    'category': 'Expense',
    'summary': "Ikatech Hr Expense Bevahiours",
    'author': "Ikatech",
    'website': 'https://ikatechsolutions.com/',
    'license': 'AGPL-3',
    'depends': [
        'hr_expense',
    ],
    'data': [
        'views/hr_expense_view.xml',
    ],
    'installable': True,

    'odoo-license': 'EE',

}
