# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class AgendamentoServico(models.Model):
    _name = "agendamento.servico"
    _description = "servico"
    _order="id asc"

    code = fields.Char('Codigo')
    dia_agendado = fields.Char('Dia agendado')
    cliente = fields.Many2one('res.partner', 'Cliente')
    fila = fields.Many2one('fila.fila', 'Fila')
    hora = fields.Char(string='Hora')

    state=fields.Selection([
    ('agendado','Agendado'),
    ('atendido','Atendido'),
    ('atrasado','Atrasado'),
    ('cancelado','Cancelado'),
    ],string='Status',readonly=True,default="agendado")

    def _compute_codigo_servico(self, fila=None, fila_code=None, dia=None):
        count = self.env['agendamento.servico'].search_count([('fila', '=', fila),('dia_agendado','=',dia)])
        strNumber = str(count+1)
        stringFormatted = str(fila_code) + strNumber.zfill(5)
        return stringFormatted

    def action_agendado(self):
            self.state="agendado"
            
    def action_atendido(self):
           self.state="atendido"

    def action_atrasado(self):
            self.state="atrasado"

    def action_cancelado(self):
            self.state="cancelado"

    def action_cancelar(self, agendamentoId):
        agendamento = self.env['agendamento.servico'].search([('id','=',  agendamentoId)])
        agendamento.state="cancelado"
   
    @api.model
    def create(self, vals):
        _logger.info(f"Float: {vals['dia_agendado']} !!!!!!!!!!!!!!!!!!!")
        codeFormated = self._compute_codigo_servico(vals['fila'], vals['code'], vals['dia_agendado'])
        vals['code'] = codeFormated
        res = super().create(vals)
        _logger.info(f"{vals} !!!!!!!!!!!!!!!!!!!")
        return res