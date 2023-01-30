##############################################################################
#
#
#
#
##############################################################################

{
    'name': 'Ik Account Group',
    'version': '15.0',
    'category': '',
    'summary': "",
    'author': "Ivan Porras",
    'website': '',
    'license': 'AGPL-3',
    'depends': [
        'account',
        ],
     'data': [
         'security/ik_account_group_security.xml',
         'security/ir.model.access.csv',
         'views/menu_ik_account_group_view.xml',
         'views/ik_account_group_view.xml',
         'views/account_account_view.xml',
         'views/account_move_line_view.xml',





     ],

    'installable': True,
}
