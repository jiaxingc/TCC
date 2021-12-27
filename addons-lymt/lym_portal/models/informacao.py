# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
import base64

import logging
_logger = logging.getLogger(__name__)

class MyInformação(models.TransientModel):
    _name = "lym_portal.informacao"
    _description = "Portal do Expositor: Informação"

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def get_event_sponsor(self):
        user = self.get_user()
        event_sponsor = self.env["event.sponsor"].search([("id","=",user.partner_id.event_sponsor_id.id)], limit=1)
        return {
            "event_sponsor": event_sponsor
        }

    def editing_informacao(self, params):
        user = self.get_user()
        informacao = self.env["event.sponsor"].search([("id","=",user.partner_id.event_sponsor_id.id)], limit=1)
        if not informacao:
            return { "error": "Sem permissão." }
        update_dict = dict()

        if params.get("website_description", str()):
            if len(params["website_description"]) > 200:
                return { "error": "Descrição com limite de 200 caracteres."}
            else:
                update_dict["website_description"] = params["website_description"]

        if params.get("email", str()):
            update_dict["email"] = params["email"]

        if params.get("url", str()):
            update_dict["url"] = params["url"]

        if params.get("youtube", str()):
            if not params["youtube"].startswith("http"):
                return { "error": "Youtube inválido. Exemplo de URL válida: https://www.youtube.com" }
            else:
                update_dict["youtube"] = params["youtube"]

        if params.get("linkedin", str()):
            if not params["linkedin"].startswith("http"):
                return { "error": "Linkedin inválido. Exemplo de URL válida: https://www.linkedin.com/" }
            else:
                update_dict["linkedin"] = params["linkedin"]

        if params.get("facebook", str()):
            if not params["facebook"].startswith("http"):
                return { "error": "Facebook inválido. Exemplo de URL válida: https://www.facebook.com" }
            else:
                update_dict["facebook"] = params["facebook"]

        if params.get("instagram", str()):
            if not params["instagram"].startswith("http"):
                return { "error": "Instagram inválido. Exemplo de URL válida: https://www.instagram.com" }
            else:
                update_dict["instagram"] = params["instagram"]

        if params.get("twitter", str()):
            if not params["twitter"].startswith("http"):
                return { "error": "Twitter inválido. Exemplo de URL válida: https://www.twitter.com" }
            else:
                update_dict["twitter"] = params["twitter"]

        if update_dict:
            update_dict["valid_info"] = False
            informacao.write(update_dict)

        expositor_name = user.partner_id.event_sponsor_id.name
        titulo = f'Informações Alteradas: {expositor_name}'
        message = f'As informações do Expositor{expositor_name} foram editadas e aguardam avaliação.'
        self.env["website"].browse(self._context["website_id"]).enviar_email(titulo, message)

        return { "error": False }