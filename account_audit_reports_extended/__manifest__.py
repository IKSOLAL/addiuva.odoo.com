# -*- coding: utf-8 -*-
{
    'name': "account_audit_reports_extended",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_reports'],

    # always loaded
    'data': [
        'report/report.xml',
        'wizard/account_excel_reports.xml',
    ],
    'auto_install': True,
    'application': False,
    'installable': True,

}
