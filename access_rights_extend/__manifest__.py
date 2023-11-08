# -*- coding: utf-8 -*-
{
    'name': "Access Rights Extend",

    'summary': """
       Set a default condition so that only members of the group can create master data.""",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','account','contacts','stock','analytic'],

    'data': [
        'security/res_groups.xml',
        # 'views/views.xml',
    ],

}
