# -*- coding: utf-8 -*-
{
    'name': "bi_pdf_report",

    'summary': "",

    'description': "",

    'author': "Bassam Infotech",
    'website': "http://www.bassaminfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/paperformat.xml',
        'reports/report.xml',
        'views/report_template.xml',
        'views/report_layout.xml',
    ],
    'images':[
        'static/description/icon.png',
        'static/src/img/car.png',
    ],

}
