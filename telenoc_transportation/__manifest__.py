# -*- coding: utf-8 -*-
{
    'name': "Telenoc transportation detail",
    'summary': """
        Telenoc transportation detail""",
    'description': """
        Telenoc transportation detail
    """,
    'author': "Magdy, helcon",
    'website': "http://www.yourcompany.com",
    'category': 'sale',
    'version': '0.1',
    'depends': ['sale', 'board', 'hr', 'fleet'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/transportation_seq.xml',
        'views/sale_order.xml',
        'views/transportation_detail.xml',
        'views/dashboard.xml',
        'views/fleet_view.xml',
    ],
}
