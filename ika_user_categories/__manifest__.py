# -*- coding: utf-8 -*-
{
    'name': "Ika user categories",
    'summary': """
        This module creates a field called "Categories" that is stored in the users configuration""",
    'description': """
        This module creates a field called "Categories" that is stored in the users configuration
    """,

    'author': "Ivan Porras",
    'category': 'User',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'views/res_users_view_inherit.xml',
    ],
}
