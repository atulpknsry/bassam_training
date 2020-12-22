# -*- coding: utf-8 -*-
{
    'name': "CRM to PO",

    'summary': "Generate Purchase Order from CRM",

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
    'depends': ['base','crm','purchase','sale_crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    
    ],
    
}
