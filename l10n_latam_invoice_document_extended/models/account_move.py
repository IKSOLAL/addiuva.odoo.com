
from odoo import models, api
class AccountMove(models.Model):
    _inherit = "account.move"

    @api.constrains('move_type', 'l10n_latam_document_type_id')
    def _check_invoice_type_document_type(self):
        return True