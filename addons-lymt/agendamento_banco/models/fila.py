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

    @api.constrains('code')
    def _check_unique_fila(self):
        fila_ids = self.search([]) - self
        value = [x.code.lower() for x in fila_ids]
        if self.name and self.code.lower() in value:
            raise ValidationError(_('The combination is already Exist'))
        return True