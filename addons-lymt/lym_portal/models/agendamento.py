# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class MyPortal(models.TransientModel):
    _name = "lym_portal.agendamento"
    _description = "Agendamento"

    # def get_user(self):
    #     context = self._context
    #     return self.env['res.users'].browse(context.get('uid'))