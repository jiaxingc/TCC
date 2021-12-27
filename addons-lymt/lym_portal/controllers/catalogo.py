# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyCatalogo(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/catalogos'], type='http', auth="public", website=True, sitemap=False)
    def _catalogos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.catalogo'].sudo().get_catalogos()
                return request.render("lym_portal.view_catalogos", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/catalogos/cadastro'], type='http', auth="public", website=True, sitemap=False)
    def _cadastro_catalogos(self, **post):
        if request.session.uid:
            if self._check_permission():
                return request.render("lym_portal.cadastro_catalogo", dict())
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/catalogos/edit/<int:_id>'], type='http', auth="public", website=True, sitemap=False)
    def _edit_catalogos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.catalogo'].sudo().get_catalogo(_id)
                if resp["catalogo"]:
                    if post.get("error", False):
                        resp["error"] = post["error"]
                    return request.render("lym_portal.edit_catalogo", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/catalogos/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _editing_catalogos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.catalogo'].sudo().editing_catalogo(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/catalogos/edit/{post['id']}", resp)
                else:
                    return request.redirect('/myportal/catalogos')
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/catalogos/delete/<int:_id>', type='http', auth='user', website=True, sitemap=False, methods=['GET','POST'])
    def _delete_catalogos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                http.request.env['lym_portal.catalogo'].sudo().delete_catalogo(_id)
                return request.redirect('/myportal/catalogos')
            raise NotFound()
        else:
            return request.redirect('/web/login')
