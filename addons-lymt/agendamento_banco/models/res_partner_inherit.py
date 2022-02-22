# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api
import requests
import re

import logging
_logger = logging.getLogger(__name__)

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    cpf_cnpj = fields.Char('CPF/CNPJ')
    rg = fields.Char('RG')
    vip = fields.Boolean('Vip', default=False)
    registroServicos = fields.One2many('agendamento.servico', 'cliente', string='Registro Serviços')

    @api.onchange('zip')
    def _compute_zip(self):
        for i in self:
            if i.zip and re.findall(r'^\d{8}$', i.zip):
                url = f'https://viacep.com.br/ws/{i.zip}/json/'
                try:
                    resp = requests.get(url)
                    if resp.status_code == 200 and not resp.json().get('erro', False):
                        _json = resp.json()
                        i.street = _json.get('logradouro', None)
                        i.street2 = _json.get('complemento', None)
                        i.city = _json.get('localidade', None)
                        i.country_id = i.env['res.country'].search([('code', '=', 'BR')], limit=1)
                        i.state_id = i.env['res.country.state'].search([('code', '=', _json.get('uf', None)),('country_id', '=', i.country_id.id)], limit=1)
                except:
                    _logger.error("erro ao pesquisar o CEP.")



# Email deve ser único
_sql_constraints = [
        ('email_uniq', 'unique(email)', 'Email deve ser único.')
    ]

# @api.onchange('email_id')
# def validate_mail(self):
#        if self.email_id:
#         match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_id)
#         if match == None:
#             raise ValidationError('não é um ID de e-mail válido')

# @api.multi
# def _validate_email(self):
#     for partner in self:
#         if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", partner.email) == None:
#             return False
#         return True



#CPF/CNPj deve ser unico
_sql_constraints=[
        ('cpf_cnpj_uniq','unique(cpf_cnpj)','CPF/CNPJ deve ser único.')
]

@api.constrains('cpf_cnpj')
def _check_cpf_cnpj(self):
	cpf_cnpj=self.search([('cpf_cnpj','=',self.cpf_cnpj)])
	if len(cpf_cnpj)>1:
	   ('error,o CPF/CNPJ já existe!')

#ID deve ser unico
_sql_constraints=[
        ('rg_uniq','unique(rg)','O numério de indentidade deve ser único.')
]
