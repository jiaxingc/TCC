# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyBanner(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/banners'], type='http', auth="public", website=True, sitemap=False)
    def _banners(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.banner'].sudo().get_banners()
                return request.render("lym_portal.view_banners", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/banners/cadastro'], type='http', auth="public", website=True, sitemap=False)
    def _cadastro_banners(self, **post):
        if request.session.uid:
            if self._check_permission():
                return request.render("lym_portal.cadastro_banner", dict())
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/banners/edit/<int:_id>'], type='http', auth="public", website=True, sitemap=False)
    def _edit_banners(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.banner'].sudo().get_banner(_id)
                if resp["banner"]:
                    if post.get("error", False):
                        resp["error"] = post["error"]
                    return request.render("lym_portal.edit_banner", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/banners/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _editing_banners(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.banner'].sudo().editing_banner(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/banners/edit/{post['id']}", resp)
                else:
                    return request.redirect('/myportal/banners')
            raise NotFound()
        else:
           return request.redirect('/web/login') 

    @http.route('/myportal/banners/delete/<int:_id>', type='http', auth='user', website=True, sitemap=False, methods=['GET','POST'])
    def _delete_banners(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                http.request.env['lym_portal.banner'].sudo().delete_banner(_id)
                return request.redirect('/myportal/banners')
            raise NotFound()
        else:
           return request.redirect('/web/login') 