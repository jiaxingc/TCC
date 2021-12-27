# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class MyVideo(models.TransientModel):
    _name = "lym_portal.video"
    _description = "Portal do Expositor: Vídeo"

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def get_videos(self):
        user = self.get_user()
        videos = self.env["lym_sponsor.video"].search([("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "videos": videos
        }

    def get_video(self, _id):
        user = self.get_user()
        video = self.env["lym_sponsor.video"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "video": video
        }

    def editing_video(self, params):
        user = self.get_user()
        if not 'id' in params or not 'title' in params or not 'url' in params:
            return { "error": "Campos obrigatórios não preenchidos." }
        video = self.env["lym_sponsor.video"].search([("id","=",params['id']), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if not video:
            return { "error": "Sem permissão." }

        if len(params.get("title", str())) > 75:
            return { "error": "Título com limite de 75 caracteres." }
        if not params.get("url", str()).startswith("http"):
            return { "error": "URL inválida. Exemplo de URL válida: https://www.google.com" }
            
        video.write({
            "title": params["title"],
            "url": params["url"],
            "valid": False
        })
        
        expositor_name = user.partner_id.event_sponsor_id.name
        titulo = f'Vídeo Alterado: {expositor_name}'
        message = f'Um Vídeo do Expositor {expositor_name} foi alterado e aguarda validação.'
        self.env["website"].browse(self._context["website_id"]).enviar_email(titulo, message)

        return { "error": False }

    def delete_video(self, _id):
        user = self.get_user()
        video = self.env["lym_sponsor.video"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if video:
            video.unlink()