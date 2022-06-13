from odoo import models, fields

class AgendamentoSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hora_inicio = fields.Integer(string="Horario de Atendimento")
    hora_fim = fields.Integer(string="Encerra Atendimento")