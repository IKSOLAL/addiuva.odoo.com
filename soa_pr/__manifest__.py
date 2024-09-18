# -*- coding: utf-8 -*-
{
    'name': "Soa Pr",
    'summary': """
        This module is an extension of the SOA integrations module""",
    'description': """
        This module extends the functionalities of the SOA Integrations module by adding some different features to the module.
    """,
    'author': "Ivan Porras",
    'category': 'SOA',
    'version': '0.1',
    'depends': ['base', 'soa_integrations', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/soa_pr_view_form.xml',
    ],
}
