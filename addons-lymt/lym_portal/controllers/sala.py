# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MySala(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/salas'], type='http', auth="public", website=True, sitemap=False)
    def _salas(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.sala'].sudo().get_salas()
                return request.render("lym_portal.view_salas", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    # @http.route(['/myportal/salas/cadastro'], type='http', auth="public", website=True, sitemap=False)
    # def _cadastro_salas(self, **post):
    #     if request.session.uid:
    #         if self._check_permission():
    #             resp = dict()
    #             if post.get("error", False):
    #                 resp["error"] = post["error"]
    #             return request.render("lym_portal.cadastro_sala", resp)
    #         raise NotFound()
    #     else:
    #         return request.redirect('/web/login')

    # @http.route('/myportal/salas/creating', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    # def _creating_salas(self, **post):
    #     if request.session.uid:
    #         if self._check_permission():
    #             resp = http.request.env['lym_portal.sala'].sudo().creating_sala(post)
    #             if resp.get("error", False):
    #                 return local_redirect(f"/myportal/salas/cadastro", resp)
    #             else:
    #                 return request.redirect('/myportal/salas')
    #         raise NotFound()
    #     else:
    #         return request.redirect('/web/login')

    # @http.route(['/myportal/salas/edit/<int:_id>'], type='http', auth="public", website=True, sitemap=False)
    # def _edit_salas(self, _id, **post):
    #     if request.session.uid:
    #         if self._check_permission():
    #             resp = http.request.env['lym_portal.sala'].sudo().get_sala(_id)
    #             if resp["sala"]:
    #                 if post.get("error", False):
    #                     resp["error"] = post["error"]
    #                 return request.render("lym_portal.edit_sala", resp)
    #         raise NotFound()
    #     else:
    #         return request.redirect('/web/login')

    # @http.route('/myportal/salas/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    # def _editing_salas(self, **post):
    #     if request.session.uid:
    #         if self._check_permission():
    #             resp = http.request.env['lym_portal.sala'].sudo().editing_sala(post)
    #             if resp.get("error", False):
    #                 return local_redirect(f"/myportal/salas/edit/{post['id']}", resp)
    #             else:
    #                 return request.redirect('/myportal/salas')
    #         raise NotFound()
    #     else:
    #         return request.redirect('/web/login')