# -*- coding: utf-8 -*-
{
    'name': "Invoice Followup",
    'summary': """
        Follow past due invoices""",
    'description': """
    """,
    'author': "Bassam Infotech LLP",
    'website': "http://www.Bassaminfotech.com",
    'category': 'Account',
    'version': '13.0.1',
    'depends': ['base','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/bi_inovice_followup_view.xml',
        'wizards/followup_wizard.xml',
    ],
    'images': [ 
        'static/description/icon.png',
    ]
}
