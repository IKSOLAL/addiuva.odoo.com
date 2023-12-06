# -*- coding: utf-8 -*-
{
    'name': "Account Reports Extend",

    'summary': """
        Add a tag column to the reports of aged accounts""",

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_reports'],

    # always loaded
    'data': [
        'views/views.xml',
    ],

}
