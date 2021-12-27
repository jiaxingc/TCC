# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from PIL import Image
import base64
import io
import re

import logging
_logger = logging.getLogger(__name__)

class MyRepresentante(models.TransientModel):
    _name = "lym_portal.representante"
    _description = "Portal do Expositor: Representante"

    def get_portal(self, field):
        context = dict(field._context)
        context.update({"default_groups": "Portal"})
        field = field.with_context(context)
        return field

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def check_email(self, email):
        if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email)):
            return True
        else:
            return False

    def get_representantes(self):
        user = self.get_user()
        representantes = self.env["res.users"].search([("event_sponsor_id","=",user.partner_id.event_sponsor_id.id),("partner_id.is_event_sponsor_admin","=",False)])
        return {
            "representantes": representantes
        }

    def get_representante(self, _id):
        user = self.get_user()
        representante = self.env["res.users"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id),("partner_id.is_event_sponsor_admin","=",False)])
        return {
            "representante": representante
        }

    def creating_representante(self, params):
        user = self.get_user()
        if not 'name' in params or not 'email' in params or not 'new_password' in params or not 'img' in params:
            return { "error": "Campos obrigatórios não preenchidos." }
        representante = self.env["res.users"].search([("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if not representante:
            return { "error": "Não é possível cadastrar sem ser um representante." }

        _img = None
        if params.get("img", False):
            try:
                _img = params["img"].read()
                pil_img = Image.open(io.BytesIO(_img))
                # if pil_img.size[0] != 150 or pil_img.size[1] != 150:
                #     return { "error": "Imagem não é do tamanho 150x150." }
                if pil_img.format not in ['PNG', 'JPEG']:
                    return { "error": "Imagem não é está no formato PNG/JPEG." }
                b64 = base64.b64encode(_img)
                # _img= tools.image_process(b64, size=(150,150), verify_resolution=True)
                _img = tools.image_process(b64, verify_resolution=True)
            except Exception:
                return { "error": "Imagem inválida." }

        if not self.check_email(params["email"]):
            return { "error": "Email inválido." }

        _user = self.get_portal(self.env["res.users"])
        _user = user.create({
            "name": params["name"],
            "login": params["email"],
            "image_1920": _img,
            "new_password": params["new_password"],
            "password": params["new_password"],
            "event_sponsor_id": user.partner_id.event_sponsor_id.id,
            "groups_id": [(6, 0, [self.env.ref('base.group_portal').id])]
        })

        partner = _user.partner_id
        partner.write({
            # "mobile": params["mobile"],
            "company_type": "person"
        })

        self.env["event.meeting.room"].create({
            "event_id": _user.partner_id.event_sponsor_id.event_id.id,
            "event_sponsor_id": _user.partner_id.event_sponsor_id.id,
            "users_id": _user.id,
            "name": _user.name,
            "room_type": "representante",
            "is_pinned": True
        })

        return { "error": False }

    def editing_representante(self, params):
        user = self.get_user()
        if not 'name' in params or not 'email' in params:
            return { "error": "Campos obrigatórios não preenchidos." }
        representante = self.env["res.users"].search([("id","=",params['id']), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if not representante:
            return { "error": "Não é possível editar sem ser um representante." }

        _img = None
        if params.get("img", False):
            try:
                _img = params["img"].read()
                pil_img = Image.open(io.BytesIO(_img))
                # if pil_img.size[0] != 150 or pil_img.size[1] != 150:
                #     return { "error": "Imagem não é do tamanho 150x150." }
                if pil_img.format not in ['PNG', 'JPEG']:
                    return { "error": "Imagem não é está no formato PNG/JPEG." }
                b64 = base64.b64encode(_img)
                # _img= tools.image_process(b64, size=(150,150), verify_resolution=True)
                _img = tools.image_process(b64, verify_resolution=True)
            except Exception:
                return { "error": "Imagem inválida." }

        if not self.check_email(params["email"]):
            return { "error": "Email inválido." }

        _new_password = None
        if "new_password" in params and params["new_password"]:
            _new_password = params["new_password"]

        update_user = {
            "name": params["name"],
            "login": params["email"]
        }
        if _img:
            update_user["image_1920"] = _img
        if _new_password:
            update_user["new_password"] = _new_password
        
        _user = self.get_portal(self.env["res.users"])
        _user = _user.search([("id","=",params["id"])], limit=1)
        _user.write(update_user)

        partner = _user.partner_id
        update_partner = {
            "name": params["name"]
            # "mobile": params["mobile"]
        }
        if _img:
            update_partner["image_1920"] = _img
        partner.write(update_partner)

        return { "error": False }

    # def delete_representante(self, _id):
    #     user = self.get_user()
    #     representante = self.env["res.users"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
    #     if representante:
    #         representante.unlink()