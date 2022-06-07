# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class FilaFila(models.Model):
    _name='fila.fila'
    _description='Fila'

    code = fields.Char('Codigo')
    name = fields.Char('Nome')
    agendamento = fields.One2many('agendamento.servico', 'fila', string='Registro Agendamentos')

    _sql_constraints = [
        ('check_conde', 'UNIQUE(code)', 'The code name is already in use.')
    ]