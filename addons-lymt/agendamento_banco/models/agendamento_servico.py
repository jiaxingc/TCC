# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class AgendamentoServico(models.Model):
    _name = "agendamento.servico"
    _description = "servico"

    code = fields.Char('Codigo', compute='_compute_codigo_servico')
    dataAgendada = fields.Datetime('Data agendada')
    cliente = fields.Many2one('res.partner', 'Cliente')
    fila = fields.Many2one('fila.fila', 'Fila')

    @api.depends('code')
    def _compute_codigo_servico(self):
        stringFormatted = 'PAO' + '0001'
        self.code = stringFormatted

    # @api.model
    # def create(self, values):
    #     pass
    #     return super(__class__, self).create(values)