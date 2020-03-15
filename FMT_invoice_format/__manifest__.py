# -*- coding: utf-8 -*-
{
    'name': "FMT Invoice Report",
    'summary': """
        FMT Invoice Report""",
    'description': """
        FMT Invoice Report
    """,
    'author': "Magdy, helcon",
    'website': "https://telenoc.org",
    'category': 'Account',
    'version': '0.1',
    'depends': ['base', 'sale', 'account', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice.xml',
        # 'report/sales_report.xml',
        'report/invoice_report.xml',
    ],
}
