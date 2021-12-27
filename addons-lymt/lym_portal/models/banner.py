# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from PIL import Image
import base64
import io

import logging
_logger = logging.getLogger(__name__)

class MyBanner(models.TransientModel):
    _name = "lym_portal.banner"
    _description = "Portal do Expositor: Banner"

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def get_banners(self):
        user = self.get_user()
        banners = self.env["lym_sponsor.banner"].search([("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "banners": banners
        }

    def get_banner(self, _id):
        user = self.get_user()
        banner = self.env["lym_sponsor.banner"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "banner": banner
        }

    def editing_banner(self, params):
        user = self.get_user()
        if not 'img_desktop' in params or not 'img_mobile' in params:
            return { "error": "Campos obrigatórios não preenchidos." }
        banner = self.env["lym_sponsor.banner"].search([("id","=",params['id']), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if not banner:
            return { "error": "Sem permissão." }
        update_dict = dict()

        if params.get("img_desktop", False):
            try:
                _img = params["img_desktop"].read()
                pil_img = Image.open(io.BytesIO(_img))
                if pil_img.size[0] != 1110 or pil_img.size[1] != 300:
                    return { "error": "Imagem Desktop não é do tamanho 1110x300." }
                if pil_img.format not in ['PNG', 'JPEG']:
                    return { "error": "Imagem Desktop não é está no formato PNG/JPEG." }
                b64 = base64.b64encode(_img)
                update_dict["img_desktop"] = tools.image_process(b64, size=(1110,300), verify_resolution=True)
            except Exception:
                return { "error": "Imagem inválida." }
            
        if params.get("img_mobile", False):
            try:
                _img = params["img_mobile"].read()
                pil_img = Image.open(io.BytesIO(_img))
                if pil_img.size[0] != 425 or pil_img.size[1] != 364:
                    return { "error": "Imagem Mobile não é do tamanho 425x364." }
                if pil_img.format not in ['PNG', 'JPEG']:
                    return { "error": "Imagem Mobile não é está no formato PNG/JPEG." }
                b64 = base64.b64encode(_img)
                update_dict["img_mobile"] = tools.image_process(b64, size=(425,364), verify_resolution=True)
            except Exception:
                return { "error": "Imagem inválida." }

        if not update_dict:
            return False
        update_dict["valid"] = False
        banner.write(update_dict)
        
        expositor_name = user.partner_id.event_sponsor_id.name
        titulo = f'Banner Alterado: {expositor_name}'
        message = f'Um Banner do Expositor {expositor_name} foi alterado e aguarda validação.'
        self.env["website"].browse(self._context["website_id"]).enviar_email(titulo, message)

        return { "error": False }

    def delete_banner(self, _id):
        user = self.get_user()
        banner = self.env["lym_sponsor.banner"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if banner:
            banner.unlink()