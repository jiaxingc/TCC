# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class FormsAgendamento(models.TransientModel):
    _name = "lym_portal.formsagendamento"
    _description = "Forms Agendamento"

    # def get_user(self):
    #     context = self._context
    #     return self.env['res.users'].browse(context.get('uid'))
