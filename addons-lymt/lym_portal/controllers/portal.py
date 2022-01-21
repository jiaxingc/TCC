# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, route
from werkzeug.exceptions import NotFound

from odoo.addons.portal.controllers import portal

import logging
_logger = logging.getLogger(__name__)

class CustomerPortal(http.Controller):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
            return request.redirect('/')

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
            return request.redirect('/')

    @route('/my/security', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def security(self, **post):
            return request.redirect('/')

portal.CustomerPortal.home = CustomerPortal.home
portal.CustomerPortal.account = CustomerPortal.account
portal.CustomerPortal.security = CustomerPortal.security