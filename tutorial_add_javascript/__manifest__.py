{    
    'name': "tutorial_add_javascript",    
    'summary': """Example Hello World application""",    
    'description': """This is an example application to learn the basics of the JS framework.""",    
    'author': "Aaro",    
    'version': '13.0.0.1',    
    'depends': ['base', 'web'],    
    'application': True,
    'data': [
        'views/assets.xml',
        'views/views.xml',
    ],
    'qweb': [
        'static/src/xml/hello_world.xml',
    ]
}
