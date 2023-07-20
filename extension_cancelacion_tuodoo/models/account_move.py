# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_repr

import base64
import requests

from lxml import etree
from lxml.objectify import fromstring
from pytz import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    cfdi_cancel_to_cancel = fields.Boolean(
        string='Documento a cancelar',
        copy=False,
        default=False,
    )

    cancel_type_id = fields.Many2one(
        'cancel.motive',
        string='Motivo de cancelación',
        copy=False,
    )

    replace_uuid = fields.Char(string="Reemplazar Folio Fiscal", copy=False)

    code_motive = fields.Char(
        string='Code',
        related="cancel_type_id.default_code",
        store=True,
        copy=False,
    )

    ############################## Functions ###############################################

    def button_cancel_posted_moves(self):
        # OVERRIDE
        action = super(AccountMove, self).button_cancel_posted_moves()
        self.cfdi_cancel_to_cancel = True
        return action
        


    ########################################################################################