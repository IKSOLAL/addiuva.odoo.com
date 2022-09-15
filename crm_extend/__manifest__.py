# -*- coding: utf-8 -*-
{
    'name': "crm_extend",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','contacts'],

    # always loaded
    'data': [
        # 'security/rules.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
