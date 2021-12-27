# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyInformacao(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/informacoes'], type='http', auth="public", website=True, sitemap=False)
    def _edit_informacaos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.informacao'].sudo().get_event_sponsor()
                if resp["event_sponsor"]:
                    if post.get("error", False):
                        resp["error"] = post["error"]
                    return request.render("lym_portal.edit_informacao", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/informacoes/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _editing_informacaos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.informacao'].sudo().editing_informacao(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/informacoes", resp)
                else:
                    return request.redirect('/myportal')
            raise NotFound()
        else:
            return request.redirect('/web/login')