# -*- coding: utf-8 -*-
{
    'name': "Pending Accounts Report",

    'summary': """
        This module generates the report to view in excel format the pending accounts receivable and payable.
        """,

    'category': 'account',
    'version': '0.1',

    'depends': ['base','report_xlsx','account'],

    'data': [
        'security/ir.model.access.csv',
        'wizards/accounts_pending.xml',
        # 'views/views.xml',
    ],



}
