# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyCurso(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/cursos'], type='http', auth="public", website=True, sitemap=False)
    def _cursos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.curso'].sudo().get_cursos()
                return request.render("lym_portal.view_cursos", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/cursos/cadastro'], type='http', auth="public", website=True, sitemap=False)
    def _cadastro_cursos(self, **post):
        if request.session.uid:
            if self._check_permission():
                return request.render("lym_portal.cadastro_curso", dict())
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/cursos/edit/<int:_id>'], type='http', auth="public", website=True, sitemap=False)
    def _edit_cursos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.curso'].sudo().get_curso(_id)
                if resp["curso"]:
                    if post.get("error", False):
                        resp["error"] = post["error"]
                    return request.render("lym_portal.edit_curso", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/cursos/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _editing_cursos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.curso'].sudo().editing_curso(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/cursos/edit/{post['id']}", resp)
                else:
                    return request.redirect('/myportal/cursos')
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/cursos/delete/<int:_id>', type='http', auth='user', website=True, sitemap=False, methods=['GET','POST'])
    def _delete_cursos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                http.request.env['lym_portal.curso'].sudo().delete_curso(_id)
                return request.redirect('/myportal/cursos')
            raise NotFound()
        else:
            return request.redirect('/web/login')