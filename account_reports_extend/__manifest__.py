# -*- coding: utf-8 -*-
{
    'name': "Account Reports Extend",

    'summary': """
        Add a tag column to the reports of aged accounts""",

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_reports', 'report_xml'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/report_move_assistan.xml',
        'views/account_assistant.xml',
        
    ],

}
