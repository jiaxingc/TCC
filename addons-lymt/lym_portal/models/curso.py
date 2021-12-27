# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class MyCurso(models.TransientModel):
    _name = "lym_portal.curso"
    _description = "Portal do Expositor: Curso"

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def get_cursos(self):
        user = self.get_user()
        cursos = self.env["lym_sponsor.curso"].search([("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "cursos": cursos
        }

    def get_curso(self, _id):
        user = self.get_user()
        curso = self.env["lym_sponsor.curso"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "curso": curso
        }

    def editing_curso(self, params):
        user = self.get_user()
        if not 'id' in params or not 'title' in params or not 'description' in params or not 'url' in params:
            return { "error": "Campos obrigatórios não preenchidos." }
        curso = self.env["lym_sponsor.curso"].search([("id","=",params['id']), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if not curso:
            return { "error": "Sem permissão." }

        if len(params.get("title", str())) > 60:
            return { "error": "Título com limite de 60 caracteres." }
        if len(params.get("description", str())) > 125:
            return { "error": "Descrição com limite de 125 caracteres." }
        if not params.get("url", str()).startswith("http"):
            return { "error": "URL inválida. Exemplo de URL válida: https://www.google.com" }

        curso.write({
            "title": params["title"],
            "url": params["url"],
            "description": params["description"],
            "valid": False
        })
        
        expositor_name = user.partner_id.event_sponsor_id.name
        titulo = f'Curso Alterado: {expositor_name}'
        message = f'Um Curso do Expositor {expositor_name} foi alterado e aguarda validação.'
        self.env["website"].browse(self._context["website_id"]).enviar_email(titulo, message)

        return { "error": False }

    def delete_curso(self, _id):
        user = self.get_user()
        curso = self.env["lym_sponsor.curso"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if curso:
            curso.unlink()