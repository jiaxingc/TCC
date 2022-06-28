# -*- coding: utf-8 -*-
import werkzeug.urls
import werkzeug.wrappers
from string import capwords
from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.exceptions import ValidationError, UserError
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

    @http.route(['/agendamento_ok'], type='http', auth="public", website=True, sitemap=False)
    def agendamento_ok(self, **post):
        uid = request.uid
        user = request.env['res.users'].sudo().search([('id','=', uid)])
        agendamentoAtivo = request.env['agendamento.servico'].sudo().search([('cliente', '=', uid), ('state','!=','cancelado'), ('state','!=','cancelado')])
        vals = {}
<<<<<<< HEAD
=======
        configObj = request.env['res.config.settings'].sudo()
        try:
            configObj = configObj.search([])[-1]
            _logger.warning(f"!!! {configObj} type: {type(configObj)}")
        except:
            _logger.warning(f"!!! erro")
        config_last_record = configObj
        days = []

        if config_last_record.sunday:
            days.append(config_last_record._fields['sunday'].string)
        if config_last_record.monday:
            days.append(config_last_record._fields['monday'].string)
        if config_last_record.tuesday:
            days.append(config_last_record._fields['tuesday'].string)
        if config_last_record.wednesday:
            days.append(config_last_record._fields['wednesday'].string)
        if config_last_record.thursday:
            days.append(config_last_record._fields['thursday'].string)
        if config_last_record.friday:
            days.append(config_last_record._fields['friday'].string)
        if config_last_record.saturday:
            days.append(config_last_record._fields['saturday'].string)

        _logger.info(f"### {days} !!!")

>>>>>>> ceb6693ff9200e08cad2e25b4df95960847e9038
        fila = request.env['fila.fila']
        filaId = fila.sudo().search([('code','=', post.get('fila_type', None))])
        vals['fila'] = filaId.id

        if agendamentoAtivo:
            raise UserError("Já há um agendamento ativo!")
        else:
            if vals['fila']:
                dia= post.get('dia', None)
                vals['code'] = filaId.code
                vals['cliente'] = user.partner_id.id
                vals['dia_agendado'] = dia
                vals['hora'] = post.get('hour', None)
                http.request.env['agendamento.servico'].sudo().create(vals)

        if request.session.uid:
            return request.render("website_form.contactus_thanks")
        else:
            return request.redirect('/web/login')

    @http.route(['/forms_agendamento'], type='http', auth='user', website=True, csrf=False)
    def service_agendamento(self, **post):

        uid = request.uid
        user = request.env['res.users'].sudo().search([('id','=', uid)])
        agendamentoAtivo = request.env['agendamento.servico'].sudo()
        agendamentoAtivoId = agendamentoAtivo.search([('cliente', '=', user.partner_id.id), ('state','!=','cancelado')])

        if agendamentoAtivoId:
            raise ValidationError("Já há um agendamento ativo!")
        else:
            configObj = request.env['res.config.settings'].sudo()
            try:
                configObj = configObj.search([])[-1]
            except:
                _logger.warning(f"!!! erro")
            config_last_record = configObj
            days = []

            if config_last_record.sunday:
                days.append(config_last_record._fields['sunday'].string)
            if config_last_record.monday:
                days.append(config_last_record._fields['monday'].string)
            if config_last_record.tuesday:
                days.append(config_last_record._fields['tuesday'].string)
            if config_last_record.wednesday:
                days.append(config_last_record._fields['wednesday'].string)
            if config_last_record.thursday:
                days.append(config_last_record._fields['thursday'].string)
            if config_last_record.friday:
                days.append(config_last_record._fields['friday'].string)
            if config_last_record.saturday:
                days.append(config_last_record._fields['saturday'].string)

            fila = request.env['fila.fila']

            res = {
                    'filas':fila.sudo().search([]),
                    'hora_inicio': config_last_record.hora_inicio,
                    'hora_fim': config_last_record.hora_fim,
                    'days': days,
                }
                    
            if request.session.uid:
                return request.render("agendamento_banco.lym_myportal_forms_Agendamento", res)
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

    @http.route(['/cancelar'], type='http', auth="public", website=True, sitemap=False)
    def _cancelar(self, **post):
        agendamento = request.env['agendamento.servico']
        agendamentoId = agendamento.sudo().search([('id','=', post.get('agendamento', None))])
        http.request.env['agendamento.servico'].sudo().action_cancelar(agendamentoId.id)
        return request.redirect("/historico")

    @http.route(['/form/success'], type='http', auth="public", website=True, csrf=True)
    def success_page(self, **post):
        return http.request.render('form.success', post)