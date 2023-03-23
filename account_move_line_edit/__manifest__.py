# -*- coding: utf-8 -*-
{
    'name': "Account Move Line Edit",

    'description': """
       wizard to update the supplier, general account and analytical accounts of journal entries and analytical entries.
    """,

    'author': "Ikatech",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
