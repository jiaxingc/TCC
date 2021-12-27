# -*- coding: utf-8 -*-
 
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
 
import logging
_logger = logging.getLogger(__name__)

class MyPortal(http.Controller):

    # def _check_permission(self):
    #     return http.request.env['lym_portal.myportal'].sudo()
        # .check_permission()
 
    @http.route(['/myportal'], type='http', auth="public", website=True, sitemap=False)
    def _myportal(self, **post):
        if request.session.uid:
            # permission = self._check_permission()
            portal = http.request.env['lym_portal.myportal'].sudo()
            return request.render("lym_portal.lym_myportal")
            # if permission:
                
            # raise NotFound()
        else:
            return request.redirect('/web/login')
    