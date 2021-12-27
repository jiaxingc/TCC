# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from PIL import Image
import base64
import io

import logging
_logger = logging.getLogger(__name__)

class MyProduto(models.TransientModel):
    _name = "lym_portal.produto"
    _description = "Portal do Expositor: Produto"

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def get_produtos(self):
        user = self.get_user()
        produtos = self.env["product.template"].search([("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "produtos": produtos
        }

    def get_produto(self, _id):
        user = self.get_user()
        produto = self.env["product.template"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        return {
            "produto": produto
        }

    def editing_produto(self, params):
        user = self.get_user()
        if not 'id' in params or not 'name' in params or not 'list_price' in params or not 'url' in params or not 'description_sale' in params:
            return { "error": "Campos obrigatórios não preenchidos" }
        produto = self.env["product.template"].search([("id","=",params['id']), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if not produto:
            return { "error": "Sem permissão." }

        if len(params.get("name", str())) > 25:
            return { "error": "Nome com limite de 25 caracteres." }
        if len(params.get("description_sale", str())) > 70:
            return { "error": "Descrição com limite de 70 caracteres." }
        if not params.get("url", str()).startswith("http"):
            return { "error": "URL inválida. Exemplo de URL válida: https://www.google.com" }
        
        update_dict = {
            "name": params["name"],
            "list_price": params["list_price"],
            "url": params["url"],
            "description_sale": params["description_sale"],
            "valid": False
        }

        if params.get("image_1920", False):
            try:
                _img = params["image_1920"].read()
                pil_img = Image.open(io.BytesIO(_img))
                if pil_img.size[0] != 150 or pil_img.size[1] != 150:
                    return { "error": "Imagem não é do tamanho 150x150." }
                if pil_img.format not in ['PNG', 'JPEG']:
                    return { "error": "Imagem não é está no formato PNG/JPEG." }
                b64 = base64.b64encode(_img)
                update_dict["image_1920"] = tools.image_process(b64, size=(150,150), verify_resolution=True)
            except Exception:
                return { "error": "Imagem inválida." }

        produto.write(update_dict)

        expositor_name = user.partner_id.event_sponsor_id.name
        titulo = f'Produto Alterado: {expositor_name}'
        message = f'Um Produto do Expositor {expositor_name} foi alterado e aguarda validação.'
        self.env["website"].browse(self._context["website_id"]).enviar_email(titulo, message)
        
        return { "error": False }

    def delete_produto(self, _id):
        user = self.get_user()
        produto = self.env["product.template"].search([("id","=",_id), ("event_sponsor_id","=",user.partner_id.event_sponsor_id.id)])
        if produto:
            produto.unlink()