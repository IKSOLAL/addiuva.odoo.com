
{
    "name": "SOA Integrations",
    "version": "15.0.0.0.1",
    "category": "SOA",
    "summary": "Modulo de integración SOA - ODOO",
    "author": "Ikatech Solutions",
    "maintainers": ["veronicadelgadillo"],
    "website": "https://ikatechsolutions.com",
    "depends": [
            'stock',
            'account'
        ],
    "data": [
        'security/ir.model.access.csv'
        ,'views/res_company_view.xml'
        ,'views/category_view.xml'
        ,'views/menus_view.xml'
        ,'views/product_view.xml'
    ],
    "installable": True,
}
