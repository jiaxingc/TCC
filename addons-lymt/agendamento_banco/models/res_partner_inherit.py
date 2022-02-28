# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
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

    @api.constrains('cpf_cnpj', 'rg')
    def _check_unique_fila(self):
        resPartnersIds = self.search([]) - self
        valueCpfCnpj = [x.cpf_cnpj for x in resPartnersIds]
        valueRg = [x.rg for x in resPartnersIds]
        if self.name and self.cpf_cnpj in valueCpfCnpj:
            raise ValidationError(_('The combination CPF is already Exist'))
        elif self.name and self.rg in valueRg:
            raise ValidationError(_('The combination RG is already Exist'))
        return True