#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright (c) 2018 aquíH S.A. All Rights Reserved.
# José Rodrigo Fernández Menegazzo, aquíH S.A.
# (http://www.aquih.com)
#
# This module provides a minimal El Salvador chart of accounts that can be use
# to build upon a more complex one.  It also includes a chart of taxes.
#
# This module is based on the GT chart of accounts:
#
# This module works with Odoo 12
#

{
    'name': 'El Salvador - Accounting',
    'version': '1.0',
    'category': 'Localization',
    'description': """
This is the base module to manage the accounting chart for El Salvador.
Flag icon: By Cobaltous - Own work, CC BY-SA 4.0, https://commons.wikimedia.org/w/index.php?curid=58240706
=====================================================================

Agrega una nomenclatura contable para El Salvador. También icluye impuestos.
Adds accounting chart for El Salvador. It also includes taxes.""",
    'author': 'José Rodrigo Fernández Menegazzo',
    'website': 'http://www.aquih.com/',
    'depends': ['base', 'account'],
    'data': [
        'data/l10n_sv_chart_data.xml',
        'data/account.account.template.csv',
        'data/l10n_gt_chart_post_data.xml',
        'data/account_data.xml',
        'data/account_chart_template_data.xml',
        'views/partner_views.xml',
        'security/ir.model.access.csv',
    ],
}
