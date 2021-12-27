# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyRepresentante(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/representantes'], type='http', auth="public", website=True, sitemap=False)
    def _representantes(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.representante'].sudo().get_representantes()
                return request.render("lym_portal.view_representantes", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/representantes/cadastro'], type='http', auth="public", website=True, sitemap=False)
    def _cadastro_representantes(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = dict()
                if post.get("error", False):
                    resp["error"] = post["error"]
                return request.render("lym_portal.cadastro_representante", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/representantes/creating', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _creating_representantes(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.representante'].sudo().creating_representante(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/representantes/cadastro", resp)
                else:
                    return request.redirect('/myportal/representantes')
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/representantes/edit/<int:_id>'], type='http', auth="public", website=True, sitemap=False)
    def _edit_representantes(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.representante'].sudo().get_representante(_id)
                if resp["representante"]:
                    if post.get("error", False):
                        resp["error"] = post["error"]
                    return request.render("lym_portal.edit_representante", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/representantes/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _editing_representantes(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.representante'].sudo().editing_representante(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/representantes/edit/{post['id']}", resp)
                else:
                    return request.redirect('/myportal/representantes')
            raise NotFound()
        else:
            return request.redirect('/web/login')

    # @http.route('/myportal/representantes/delete/<int:_id>', type='http', auth='user', website=True, sitemap=False, methods=['GET','POST'])
    # def _delete_representantes(self, _id, **post):
    #     if self._check_permission():
    #         http.request.env['lym_portal.representante'].sudo().delete_representante(_id)
    #         return request.redirect('/myportal/representantes')
    #     raise NotFound()