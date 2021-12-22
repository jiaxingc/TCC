from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    matricula = fields.Char("Matricula")
    cpf_cnpj = fields.Char("CPF/CNPJ")
    idade = fields.Integer("Idade")
    setor = fields.Char("Setor")