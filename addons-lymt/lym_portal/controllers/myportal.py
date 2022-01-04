# -*- coding: utf-8 -*-

import json
import lxml
import requests
import werkzeug.urls
import werkzeug.wrappers

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
from odoo.http import request

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

    @http.route(['/forum/<model("forum.forum"):forum>/new','/forum/<model("forum.forum"):forum>/<model("forum.post"):post_parent>/reply'],
    type='http', auth="user", methods=['POST'], website=True)
    def post_create(self, forum, post_parent=None, **post):
        if post.get('content', '') == '<p><br></p>':
            return request.render('http_routing.http_error', {'status_code': _('Bad Request'),
            'status_message': post_parent and _('Reply should not be empty.') or _('Question should not be empty.')
                })

        post_tag_ids = forum._tag_to_write_vals(post.get('post_tags', ''))
        _logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        _logger.info(f'{post_tag_ids}')
        _logger.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


        if request.env.user.forum_waiting_posts_count:
            return werkzeug.utils.redirect("/forum/%s/ask" % slug(forum))

        new_question = request.env['forum.post'].create({'forum_id': forum.id,
        'name': post.get('post_name') or (post_parent and 'Re: %s' % (post_parent.name or '')) or '',
        'content': post.get('content', False),
        'parent_id': post_parent and post_parent.id or False,
        'tag_ids': post_tag_ids
        })
        return werkzeug.utils.redirect("/forum/%s/%s" % (slug(forum), post_parent and slug(post_parent) or new_question.id))