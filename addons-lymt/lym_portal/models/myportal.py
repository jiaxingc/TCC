# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class MyPortal(models.TransientModel):
    _name = "lym_portal.myportal"
    _description = "Portal do Expositor"

    def get_user(self):
        context = self._context
        return self.env['res.users'].browse(context.get('uid'))

    def check_permission(self):
        user = self.get_user()
        if user.partner_id.event_sponsor_id and user.partner_id.event_sponsor_id.is_exhibitor and user.partner_id.event_sponsor_id.sponsor_type_id:
            return {
                "permission": user.partner_id.event_sponsor_id.sponsor_type_id.display_ribbon_style,
                "is_event_sponsor_admin": user.is_event_sponsor_admin
            }
        return dict()
