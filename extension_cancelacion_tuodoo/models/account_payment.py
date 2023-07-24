from odoo import models, fields

import logging
_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    cfdi_cancel_to_cancel = fields.Boolean(
        string='Documento a cancelar',
        copy=False,
        default=False,
    )

    cancel_type_id = fields.Many2one(
        'cancel.motive',
        string='Motivo de cancelación',
        copy=False,
        domain=[('is_to_payment','=',True)]
    )

    replace_uuid = fields.Char(string="Reemplazar Folio Fiscal", copy=False)

    code_motive = fields.Char(
        string='Code',
        related="cancel_type_id.default_code",
        store=True,
        copy=False,

    )

