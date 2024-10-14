# -*- coding: utf-8 -*-
{
    'name': "account_extend_ikatech",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    
    'category': 'Uncategorized',
    'version': '0.1',
    
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    
    'qweb': ['static/src/xml/account_extend_ikatech.xml',],
    
    'assets': { 
        'web.assets_backend': [ 
            'https://cdn.jsdelivr.net/npm/xlsx-js-style@1.2.0/dist/xlsx.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.0/html2pdf.bundle.min.js',
            # 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
            'account_extend_ikatech/static/src/js/account_extend_ikatech.js', 
            'account_extend_ikatech/static/src/css/style_pandl.css',
        ],
        'web.assets_qweb': [
            'account_extend_ikatech/static/src/xml/account_extend_ikatech.xml',
        ],
    },
}
