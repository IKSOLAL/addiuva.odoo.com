##############################################################################
#
#
#
#
##############################################################################

{
    'name': 'SOA Integration API',
    'version': '15.0',
    'category': '',
    'summary': "",
    'author': "Ivan Porras",
    'website': '',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'account',
        'soa_integrations',
        'product',
        'stock',




        ],
     'data': [
         'security/security.xml',
         'security/ir.model.access.csv',
         'views/menu.xml',
         'views/soa_integration_api_view.xml',
         'views/account_analytic_account_view_form.xml',





     ],

    'installable': True,
}
