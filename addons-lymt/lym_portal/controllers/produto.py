# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyProduto(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/produtos'], type='http', auth="public", website=True, sitemap=False)
    def _produtos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.produto'].sudo().get_produtos()
                return request.render("lym_portal.view_produtos", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/produtos/cadastro'], type='http', auth="public", website=True, sitemap=False)
    def _cadastro_produtos(self, **post):
        if request.session.uid:
            if self._check_permission():
                return request.render("lym_portal.cadastro_produto", dict())
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/produtos/edit/<int:_id>'], type='http', auth="public", website=True, sitemap=False)
    def _edit_produtos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.produto'].sudo().get_produto(_id)
                if resp["produto"]:
                    if post.get("error", False):
                        resp["error"] = post["error"]
                    return request.render("lym_portal.edit_produto", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/produtos/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _editing_produtos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.produto'].sudo().editing_produto(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/produtos/edit/{post['id']}", resp)
                else:
                    return request.redirect('/myportal/produtos')
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/produtos/delete/<int:_id>', type='http', auth='user', website=True, sitemap=False, methods=['GET','POST'])
    def _delete_produtos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                http.request.env['lym_portal.produto'].sudo().delete_produto(_id)
                return request.redirect('/myportal/produtos')
            raise NotFound()
        else:
            return request.redirect('/web/login')