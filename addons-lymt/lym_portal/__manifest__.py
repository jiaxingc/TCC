# -*- coding: utf-8 -*-
{
    'name': "TCC",
    'summary': """LYM Portal""",
    'description': """sistema bancário""",
    'author': "JiaXing",
    'website': "",
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    'depends': ['base', 'portal', 'website_form'],
    'data': [
        'security/ir.model.access.csv',
        'views/myportal.xml'

    ],
    'application': True,
    'auto_install': False
}