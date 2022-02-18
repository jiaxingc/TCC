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

    @http.route(['/minhainformacao'], type='http', auth="public", website=True, sitemap=False)
    def minhainformacao(self, **post):
        id=http.request.env.context.get('uid')
        if request.session.uid:
             minhainformacao = http.request.env['res.users'].sudo().search([('id','=',id)])
             parent_id=minhainformacao.partner_id
             cliente = http.request.env['res.partner'].sudo().search([('id','=',parent_id.id)])
        #      banco=http.request.env['res.partner.bank'].sudo().search(('id','=',parent_id.id))
        #      _logger.info(banco)
             return request.render("agendamento_banco.portal_minhainformacao",{'cliente':cliente,
        #      'banco':banco,
             }
            )
                
                # return request.render("agendamento_banco.portal_minhainformacao")
            
        else:
            return request.redirect('/web/login')






portal.CustomerPortal.home = CustomerPortal.home
portal.CustomerPortal.account = CustomerPortal.account
portal.CustomerPortal.security = CustomerPortal.security