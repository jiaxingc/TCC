# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

def _compute_codigo_servico(fila_code=None):
    stringFormatted = str(fila_code) + '0001'
    return stringFormatted

class AgendamentoServico(models.Model):
    _name = "agendamento.servico"
    _description = "servico"

    code = fields.Char('Codigo')
    dataAgendada = fields.Datetime('Data agendada')
    cliente = fields.Many2one('res.partner', 'Cliente')
    fila = fields.Many2one('fila.fila', 'Fila')

    state=fields.Selection([
    ('agendado','Agendado'),
    ('atendido','Atendido'),
    ('atrasado','Atrasado'),
    ('cancelado','Cancelado'),
    ],string='Status',readonly=True,default="agendado")

    def action_agendado(self):
            self.state="agendado"
            
    def action_atendido(self):
           self.state="atendido"

    def action_atrasado(self):
            self.state="atrasado"

    def action_cancelado(self):
            self.state="cancelado"
   

    def _register_scheduling(self, vals):
        try:
            vals['code'] = _compute_codigo_servico(vals['code'])
            res = super(AgendamentoServico, self).create(vals)
            return res
        except:
            _logger.error('Erro ao criar registro de agendamento!')