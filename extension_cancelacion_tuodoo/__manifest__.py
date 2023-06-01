# -*- coding: utf-8 -*-
{
    'name': "Extencion de cancelacion",

    'summary': """
    Agrega un catalago de motivos de cancelación dentro de contabilidad y al momento de solictar cancelación debe editar la factura y agregar el motivo en el campo indicado. Después dar en procesar.
    """,

    'description': """
        Agrega un catalago de motivos de cancelación dentro de contabilidad y al momento de solictar cancelación debe editar la factura y agregar el motivo en el campo indicado. Después dar en procesar.
    """,

    'author': "Tuodoo",
    'website': "https://tuodoo.com/",
    'version': '15.1.1',
    'depends': ['account','l10n_mx_edi'],
    'data': [
        'security/cancel_motive.xml',
        'views/cancel_motive_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'data/data.xml',
    ],
}
