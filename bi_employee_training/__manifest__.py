
{
    'name': 'Bi Employee Training',
    'version' : '13.0.1',
    'category': 'Hr',
    'summary': 'Employee can request for training',
    'license': 'AGPL-3',
    'description': """
    """,
    'author': 'Bassam Infotech LLP',
    'website': 'http://www.bassaminfotech.com/',
    'depends': ['base','hr'], 
    'data': [ 
            'security/user_groups.xml',
            'security/ir.model.access.csv',
            'views/employee_training.xml',
            'views/employee_training_wizard.xml', 
            'views/training_refusal_wizard.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}

