# -*- coding: utf-8 -*-

import werkzeug.urls
import werkzeug.wrappers
from string import capwords
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo import http, tools, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.website_profile.controllers.main import WebsiteProfile
from odoo.addons.portal.controllers.portal import _build_url_w_params

import logging
_logger = logging.getLogger(__name__)


class MyPortal(http.Controller):

    @http.route(['/myportal'], type='http', auth="public", website=True, sitemap=False)
    def _myportal(self, **post):
        if request.session.uid:
            return request.render("agendamento_banco.lym_myportal")
        else:
            return request.redirect('/web/login')

    # @http.route(['/forms_agendamento/<string:tipo>'], type='http', auth="public", website=True, sitemap=False)
    # def _formsagendamentos(self, tipo, **post):
    #     if request.session.uid:
    #         idUserSession = http.request.env.context.get('uid')
    #         minhainformacao = http.request.env['res.users'].sudo().search([('id', '=', idUserSession)])
    #         parent_id = minhainformacao.partner_id
    #         cliente = http.request.env['res.partner'].sudo().search([('id', '=', parent_id.id)])

    #         tipoFormatted = capwords(tipo.replace("_", "\t"))
    #         fila = request.env['fila.fila'].sudo().search([('name', '=', tipoFormatted)])

    #         print(f'{fila} !!!!!!!!!')

    #         return request.render("agendamento_banco.lym_myportal_forms_Agendamento")
    #     else:
    #         return request.redirect('/web/login')

    @http.route(['/forms_agendamento'], type='http', auth="public", website=True, sitemap=False)
    def _formsagendamentos(self, **post):
        uid = request.uid
        user = request.env['res.users'].sudo().search([('id','=', uid)])
        vals = {}
        fila = request.env['fila.fila']
        filaId = fila.sudo().search([('code','=', post.get('fila_type', None))])
        vals['fila'] = filaId.id
        vals['codeFront'] = filaId.code
        vals['dataAgendada'] = post.get('data_hour', '2022-02-22 12:29:23')
        vals['cliente'] = user.id
        # agendamento = request.env['agendamento.servico'].sudo()._register_scheduling(vals)
        http.request.env['agendamento.servico'].sudo()._register_scheduling(vals)
        if request.session.uid:
            return request.render("agendamento_banco.lym_myportal_forms_Agendamento",{'filas':fila.sudo().search([])})
        else:
            return request.redirect('/web/login')



    @http.route(['/agendamento'], type='http', auth="public", website=True, sitemap=False)
    def _agendamentos(self, **post):
        if request.session.uid:
            # agendamento = http.request.env['agendamento_banco.agendamento'].sudo()
            return request.render("agendamento_banco.portal_tela_agendamento")
        else:
            return request.redirect('/web/login')

    @http.route(['/servico'], type='http', auth="public", website=True, sitemap=False)
    def _servico(self, **post):
        if request.session.uid:
            # servico = http.request.env['agendamento_banco.servico'].sudo()
            return request.render("agendamento_banco.portal_tela_servico")
        else:
            return request.redirect('/web/login')

    # @http.route(['/filapadrao'], type='http', auth="public", website=True, sitemap=False)
    # def _filapadrao(self, **post):
    #     if request.session.uid:
    #         # fila_padrao = http.request.env['agendamento_banco.filapadrao'].sudo()
    #         return request.render("agendamento_banco.lym_myportal_fila_padrao")
    #     else:
    #         return request.redirect('/web/login')

    # @http.route(['/filaprioridade'], type='http', auth="public", website=True, sitemap=False)
    # def _filaprioridade(self, **post):
    #     if request.session.uid:
    #         # fila_prioridade = http.request.env['agendamento_banco.filaprioridade'].sudo()
    #         return request.render("agendamento_banco.portal_fila_prioridade")
    #     else:
    #         return request.redirect('/web/login')

    @http.route(['/forum/<model("forum.forum"):forum>/new', '/forum/<model("forum.forum"):forum>/<model("forum.post"):post_parent>/reply'],
                type='http', auth="user", methods=['POST'], website=True)
    def post_create(self, forum, post_parent=None, **post):
        if post.get('content', '') == '<p><br></p>':
            return request.render('http_routing.http_error', {'status_code': _('Bad Request'),
                                                              'status_message': post_parent and _('Reply should not be empty.') or _('Question should not be empty.')
                                                              })

        post_tag_ids = forum._tag_to_write_vals(post.get('post_tags', ''))
        _logger.info(post_tag_ids)

        reclamacao = forum._tag_to_write_vals(post.get('reclamacao', ''))
        if len(reclamacao) > 1:
            post_tag_ids.append(reclamacao[1])
        elif len(reclamacao[0][2]) == 1:
            post_tag_ids[0][2].append(reclamacao[0][2][0])

        sugestao = forum._tag_to_write_vals(post.get('sugestao', ''))
        if len(sugestao) > 1:
            post_tag_ids.append(sugestao[1])
        elif len(sugestao[0][2]) == 1:
            post_tag_ids[0][2].append(sugestao[0][2][0])

        outro = forum._tag_to_write_vals(post.get('outro', ''))
        if len(outro) > 1:
            post_tag_ids.append(outro[1])
        elif len(outro[0][2]) == 1:
            post_tag_ids[0][2].append(outro[0][2][0])

        if request.env.user.forum_waiting_posts_count:
            return werkzeug.utils.redirect("/forum/%s/ask" % slug(forum))

        new_question = request.env['forum.post'].create({'forum_id': forum.id,
                                                         'name': post.get('post_name') or (post_parent and 'Re: %s' % (post_parent.name or '')) or '',
                                                         'content': post.get('content', False),
                                                         'parent_id': post_parent and post_parent.id or False,
                                                         'tag_ids': post_tag_ids
                                                         })

        return werkzeug.utils.redirect("/forum/%s/%s" % (slug(forum), post_parent and slug(post_parent) or new_question.id))
