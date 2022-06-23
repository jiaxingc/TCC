from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class AgendamentoSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hora_inicio = fields.Integer(string="Horario de Atendimento")
    hora_fim = fields.Integer(string="Encerra Atendimento")

    sunday = fields.Boolean(string="Domingo")
    monday = fields.Boolean(string="Segunda")
    tuesday = fields.Boolean(string="Terça")
    wednesday = fields.Boolean(string="Quarta")
    thursday = fields.Boolean(string="Quinta")
    friday = fields.Boolean(string="Sexta")
    saturday = fields.Boolean(string="Sábado")

    def set_values(self):
        super(AgendamentoSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('hora.inicio', self.hora_inicio)
        self.env['ir.config_parameter'].sudo().set_param('hora.fim', self.hora_fim)
        self.env['ir.config_parameter'].sudo().set_param('sunday', self.sunday)
        self.env['ir.config_parameter'].sudo().set_param('monday', self.monday)
        self.env['ir.config_parameter'].sudo().set_param('tuesday', self.tuesday)
        self.env['ir.config_parameter'].sudo().set_param('wednesday', self.wednesday)
        self.env['ir.config_parameter'].sudo().set_param('thursday', self.thursday)
        self.env['ir.config_parameter'].sudo().set_param('friday', self.friday)
        self.env['ir.config_parameter'].sudo().set_param('saturday', self.saturday)

    def get_values(self):
        res = super(AgendamentoSettings, self).get_values()
        inicio = self.env['ir.config_parameter'].sudo().get_param('hora.inicio')
        fim = self.env['ir.config_parameter'].sudo().get_param('hora.fim')
        sunday = self.env['ir.config_parameter'].sudo().get_param('sunday')
        monday = self.env['ir.config_parameter'].sudo().get_param('monday')
        tuesday = self.env['ir.config_parameter'].sudo().get_param('tuesday')
        wednesday = self.env['ir.config_parameter'].sudo().get_param('wednesday')
        thursday = self.env['ir.config_parameter'].sudo().get_param('thursday')
        friday = self.env['ir.config_parameter'].sudo().get_param('friday')
        saturday = self.env['ir.config_parameter'].sudo().get_param('saturday')

        res.update({
            'hora_inicio': inicio,
            'hora_fim': fim,
            'sunday': sunday,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
        })
        return res