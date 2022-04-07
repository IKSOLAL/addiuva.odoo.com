
{
    "name": "Account Move Multi-Company",
    "summary": "Allow to transfer amount to other companies",
    "version": "14.0.1.0.3",
    "category": "Accounting & Finance",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "website": "ikatech",
    "license": "AGPL-3",
    "depends": [
        "account_invoice_consolidated",
    ],
    "data": [
        "security/ir_rule.xml",
        "views/account_move_view.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["max3903"],
}
