# -*- coding: utf-8 -*-
{
    'name': "Provision Accounts Report",

    'summary': """
        This module generates the report to view in excel format the Provision accounts receivable and payable.
        """,

    'category': 'account',
    'version': '0.1',

    'depends': ['base','report_xlsx','account'],

    'data': [
        'security/ir.model.access.csv',
        'wizards/accounts_provision.xml',
        # 'views/views.xml',
    ],



}
