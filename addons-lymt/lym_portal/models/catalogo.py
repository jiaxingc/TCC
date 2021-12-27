# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from PIL import Image
import base64
import io

import logging
_logger = logging.getLogger(__name__)

class MyCatalogo(models.TransientModel):
    _name = "lym_portal.catalogo"
    _description = "Portal do Expositor: Catálogo"

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def get_catalogos(self):
        user = self.get_user()
        catalogos = self.env["lym_sponsor.catalogo"].search([("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "catalogos": catalogos
        }

    def get_catalogo(self, _id):
        user = self.get_user()
        catalogo = self.env["lym_sponsor.catalogo"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "catalogo": catalogo
        }

    def editing_catalogo(self, params):
        user = self.get_user()
        if not 'id' in params or not 'title' in params or not 'description' in params:
            return { "error": "Campos obrigatórios não preenchidos." }
        catalogo = self.env["lym_sponsor.catalogo"].search([("id","=",params['id']), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if not catalogo:
            return { "error": "Sem permissão." }

        if len(params.get("Título", str())) > 25:
            return { "error": "Título com limite de 25 caracteres." }
        if len(params.get("description_sale", str())) > 125:
            return { "error": "Descrição com limite de 125 caracteres." }

        update_dict = {
            "title": params["title"],
            "description": params["description"],
            "valid": False
        }

        if params.get("img", False):
            try:
                _img = params["img"].read()
                pil_img = Image.open(io.BytesIO(_img))
                if pil_img.size[0] != 425 or pil_img.size[1] != 240:
                    return { "error": "Imagem não é do tamanho 425x240." }
                if pil_img.format not in ['PNG', 'JPEG']:
                    return { "error": "Imagem não é está no formato PNG/JPEG." }
                b64 = base64.b64encode(_img)
                update_dict["img"] = tools.image_process(b64, size=(425,240), verify_resolution=True)
            except Exception:
                return { "error": "Imagem inválida." }

        if "catalogo" in params and params["catalogo"]:
            try:
                b = params["catalogo"].read()
                if b[0:4] != b'%PDF':
                    return { "error": 'O catálogo não é um PDF.' }
                update_dict["catalogo"] = base64.b64encode(b)
            except Exception:
                pass

        catalogo.write(update_dict)
        
        expositor_name = user.partner_id.event_sponsor_id.name
        titulo = f'Catálogo Alterado: {expositor_name}'
        message = f'Um Catálogo do Expositor {expositor_name} foi alterado e aguarda validação.'
        self.env["website"].browse(self._context["website_id"]).enviar_email(titulo, message)

        return { "error": False }

    def delete_catalogo(self, _id):
        user = self.get_user()
        catalogo = self.env["lym_sponsor.catalogo"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if catalogo:
            catalogo.unlink()
