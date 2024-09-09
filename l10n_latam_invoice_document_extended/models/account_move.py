
from odoo import models, api
class AccountMove(models.Model):
    _inherit = "account.move"

    @api.constrains('state', 'l10n_latam_document_type_id')
    def _check_l10n_latam_documents(self):
       return True