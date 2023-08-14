
{
    "name": "SOA Integrations",
    "version": "1.3",
    "category": "SOA",
    "summary": "Modulo de integración SOA - Odoo",
    "author": "Ikatech Solutions",
    "maintainers": ["veronicadelgadillo"],
    "website": "https://ikatechsolutions.com",
    "depends": [
            'stock',
            'account',
            'base',
            'product',
            'purchase',
        ],
    "data": [
        'security/integrations_group_security.xml',
        'security/ir.model.access.csv'
        ,'views/res_company_view.xml'
        ,'views/category_view.xml'
        ,'views/menus_view.xml'
        ,'views/product_view.xml'
        ,'views/planes_view.xml'
        ,'views/plan_servicio_view.xml'
        ,'views/account_move_view.xml'
        ,'views/purchase_order_view.xml'
        ,'views/account_analytic_account_view_form.xml'
        ,'views/soa_integration_api_view.xml'
        ,'views/res_partner_view_form.xml'
        
    ],
    "installable": True
}
