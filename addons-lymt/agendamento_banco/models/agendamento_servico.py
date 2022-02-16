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

    # @api.depends()
    # def _compute_codigo_servico(self):
    #     pass