{
    'name': "Import MX XML purchase invoice",
    'summary': """""",
    'description': """
    """,
    'author': "Genivet Systems",
    'license': 'OPL-1',
    'category': 'Location',
    'version': '15.0.0.0.1',
    'currency': 'USD',
    'depends': [
        'base',
        'account',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data_sequence.xml',
        'views/account_move_views.xml',
        'views/xml_import_invoice_views.xml',
        'views/portal_templates.xml',
        'wizard/xml_import_wizard_views.xml',
    ],
    'external_dependencies': {
        'python': [
            'cfdiclient',
        ],
    },
}
