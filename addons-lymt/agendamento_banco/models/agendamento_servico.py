# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class AgendamentoServico(models.Model):
    _name = "agendamento.servico"
    _description = "servico"

    code = fields.Char('Codigo')
    dataAgendada = fields.Datetime('Data agendada')
    cliente = fields.Many2one('res.partner', 'Cliente')
    fila = fields.Many2one('fila.fila', 'Fila')

    def _compute_codigo_servico(fila_code=None, **kw):
        stringFormatted = fila_code + '0001'
        return stringFormatted

    def _register_scheduling(self, vals):
        # vals['code'] = self._compute_codigo_servico(vals['codeFront'])
        # res = agendamento.create(vals)
        print(f"{vals} !!!!!!!!!!!!!!!!!!!!!!")
        # return res