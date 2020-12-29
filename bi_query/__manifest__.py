# -*- coding: utf-8 -*-
{
    'name': "bi_query",

    'summary': "",

    'description': "",

    'author': "Bassam Infotech LLP",
    'website': "http://www.bassaminfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'wizards/bi_query_wizard.xml',
        'reports/reports.xml',
        'reports/report_template.xml',
        'reports/report_layout.xml',
        
    ],
}
