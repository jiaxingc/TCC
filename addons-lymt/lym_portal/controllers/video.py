# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request, local_redirect
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyVideo(http.Controller):

    def _check_permission(self):
        return http.request.env['lym_portal.myportal'].sudo().check_permission()

    @http.route(['/myportal/videos'], type='http', auth="public", website=True, sitemap=False)
    def _videos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.video'].sudo().get_videos()
                return request.render("lym_portal.view_videos", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/videos/cadastro'], type='http', auth="public", website=True, sitemap=False)
    def _cadastro_videos(self, **post):
        if request.session.uid:
            if self._check_permission():
                return request.render("lym_portal.cadastro_video", dict())
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route(['/myportal/videos/edit/<int:_id>'], type='http', auth="public", website=True, sitemap=False)
    def _edit_videos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.video'].sudo().get_video(_id)
                if resp["video"]:
                    if post.get("error", False):
                        resp["error"] = post["error"]
                    return request.render("lym_portal.edit_video", resp)
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/videos/editing', type='http', auth='user', website=True, sitemap=False, methods=['POST'], cors='*', csrf=False)
    def _editing_videos(self, **post):
        if request.session.uid:
            if self._check_permission():
                resp = http.request.env['lym_portal.video'].sudo().editing_video(post)
                if resp.get("error", False):
                    return local_redirect(f"/myportal/videos/edit/{post['id']}", resp)
                else:
                    return request.redirect('/myportal/videos')
            raise NotFound()
        else:
            return request.redirect('/web/login')

    @http.route('/myportal/videos/delete/<int:_id>', type='http', auth='user', website=True, sitemap=False, methods=['GET','POST'])
    def _delete_videos(self, _id, **post):
        if request.session.uid:
            if self._check_permission():
                http.request.env['lym_portal.video'].sudo().delete_video(_id)
                return request.redirect('/myportal/videos')
            raise NotFound()
        else:
            return request.redirect('/web/login')