import logging
import re

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"


    customer_software_id = fields.Many2one(comodel_name='l10n_co_edi_jorels.customer_software',
                                           string="Customer software", copy=False, ondelete='RESTRICT')
