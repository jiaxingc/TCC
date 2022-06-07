# -*- coding: utf-8 -*-
{
    'name': "TCC",
    'summary': """Apresentação de TCC""",
    'description': """sistema bancário""",
    'author': "JiaXing",
    'website': "",
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    'depends': ['base', 'portal', 'website_form','website_forum', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/myportal.xml',
        'views/menu.xml',
        'views/forum_tcc.xml',
        'views/forms_agendamento.xml',
        'views/agendamento_template.xml',
        'views/register.xml',
        'views/res_partner.xml',
        'views/agendamento_view.xml',
        'views/tela_servico.xml',
        'views/minhainformacao.xml',
        'views/fila_view.xml',
        'views/historico.xml'
    ],
    'application': True,
    'auto_install': False
}