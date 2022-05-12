import base64
import logging

import werkzeug

import odoo.http as http
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_is_zero
_logger = logging.getLogger(__name__)


class InvoiceUploadController(http.Controller):

    @http.route("/upload/invoice", type="http", auth="user", website=True)
    def create_new_invoice(self, **kw):
        return http.request.render(
            "l10n_mx_xml_invoice.portal_upload_invoice",
        )

    @http.route("/submitted/invoice", type="http", auth="user", website=True, csrf=True)
    def submit_ticket(self, **kw):
        if kw.get("attachment"):
            for c_file in request.httprequest.files.getlist("attachment"):
                data = c_file.read()
                if c_file.filename:
                    if not 'xml' in c_file.filename:
                        raise ValidationError('Por favor, adjunte un archivo con formato XML')
                    journal_id = request.env['account.journal'].sudo().search([('type', '=', 'purchase'),
                                                           ('company_id', '=', request.env.user.company_id.id)], limit=1)

                    xml_import_invoice_id =  request.env['xml.import.invoice'].sudo().create({
                        'journal_id':journal_id.id,
                        'account_id':journal_id.default_account_id.id
                     })

                    xml_import_invoice_id.write({
                        'xml_table_ids': [(0, None, {
                            'xml': base64.b64encode(data)
                        })]
                    })
                    xml_import_invoice_id.validate_xml()
                    for line in xml_import_invoice_id.xml_table_ids:
                        if line.is_duplicate:
                            raise ValidationError(line.status)

                    xml_import_invoice_id.create_xml_invoice()
                    invoices = request.env['account.move'].sudo().search([
                        ('xml_import_invoice_id','=',xml_import_invoice_id.id)])
                    for i in invoices:
                        if kw.get('purchase_id'):
                            purchase_id = kw.get('purchase_id')
                            purchase_obj = request.env['purchase.order'].sudo().browse(int(purchase_id))
                            precision = request.env['decimal.precision'].precision_get('Product Unit of Measure')

                            i.write({'invoice_line_ids': False})
                            order = purchase_obj.with_company(purchase_obj.company_id)
                            pending_section = None
                            # Invoice values.
                            invoice_vals = order._prepare_invoice()
                            # Invoice line values (keep only necessary sections).
                            for line in order.order_line:
                                if line.display_type == 'line_section':
                                    pending_section = line
                                    continue
                                if not float_is_zero(line.qty_to_invoice, precision_digits=precision):
                                    if pending_section:
                                        invoice_vals['invoice_line_ids'].append(
                                            (0, 0, pending_section._prepare_account_move_line()))
                                        pending_section = None
                                    invoice_vals['invoice_line_ids'].append((0, 0, line._prepare_account_move_line()))
                            i.write({'invoice_line_ids': invoice_vals['invoice_line_ids']})
                            i.action_post()
        return werkzeug.utils.redirect("/my/invoices")