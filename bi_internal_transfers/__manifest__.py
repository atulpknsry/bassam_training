# -*- coding: utf-8 -*-
{
    'name': "Internal Transfers",

    'summary': "",

    'description': """
        Long description of module's purpose
    """,

    'author': "Bassam Infotech LLP",
    'website': "http://www.bassaminfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/internal_transfers_views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
