from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class AgendamentoSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hora_inicio = fields.Integer(string="Horario de Atendimento")
    hora_fim = fields.Integer(string="Encerra Atendimento")

    def set_values(self):
        super(AgendamentoSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('hora.inicio', self.hora_inicio)
        self.env['ir.config_parameter'].sudo().set_param('hora.fim', self.hora_fim)

    def get_values(self):
        res = super(AgendamentoSettings, self).get_values()
        inicio = self.env['ir.config_parameter'].sudo().get_param('hora.inicio')
        fim = self.env['ir.config_parameter'].sudo().get_param('hora.fim')

        res.update({
            'hora_inicio': inicio,
            'hora_fim': fim,
        })
        return res