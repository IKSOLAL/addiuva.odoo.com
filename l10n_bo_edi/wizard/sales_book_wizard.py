# -*- coding:utf-8 -*-

from datetime import date, datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


import logging
import json
import io

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


_logger = logging.getLogger(__name__)


class SalesBookWizard(models.TransientModel):
    _name = "sales.book.wizard"
    _description = "SIN Sales Book Report Fast Wizard"

    begin_date = fields.Date(string='Begin Date', required=True)

    end_date = fields.Date(string='End Date', required=True)

    report_types = fields.Selection([
        ('pdf', 'PDF'),
        ('xlsx', 'EXCEL')
    ], string='Report Types')

    # def trigger_report(self):

    #     invoice_ids = self.env['account.move'].search(
    #         ['&', ('invoice_date_due', '>=', self.begin_date),
    #          ('invoice_date_due', '<=', self.end_date)])

    #     # _logger.info(str(invoice_ids[0].amount_total))
    #     # PENDIENTE FILTRO POR FECHAS
    #     # return self.env.ref('l10n_bo_edi.sales_book').report_action(self, data=invoice_ids)
    #     return self.env.ref('l10n_bo_edi.sales_book').report_action(self)

    def trigger_report(self):

        invoice_ids = self.env['account.move'].search(
            ['&', ('invoice_date_due', '>=', self.begin_date),
             ('invoice_date_due', '<=', self.end_date)])

        _logger.info(str(invoice_ids))
        _logger.info(str(len(invoice_ids)))

        if (len(invoice_ids) == 0):
            self.notify('No Invoices',
                        'There are no invoices in the selected range of dates', 'info')
        else:
            return self.env.ref('l10n_bo_edi.sales_book').report_action(self)

        # PENDIENTE FILTRO POR FECHAS
        # return self.env.ref('l10n_bo_edi.sales_book').report_action(self, data=invoice_ids)

    def notify(self, title, description, type):
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': (title),
                'message': description,
                'type': type,  # types: success,warning,danger,info
                'sticky': True,  # True/False will display for few seconds if false
            },
        }
        return notification

    def print_xlsx(self):

        invoice_ids = self.env['account.move'].search(
            ['&', ('invoice_date_due', '>=', self.begin_date),
             ('invoice_date_due', '<=', self.end_date)])

        if self.begin_date > self.end_date:
            raise ValidationError('Start Date must be less than End Date')

        if (len(invoice_ids) == 0):
            raise ValidationError(
                'There are no invoices in the selected range of dates')

        data = {}
        # TODO iterar sobre cada objeto y mapear lo requerido
        for index, inv in enumerate(invoice_ids):
            invoice_content = {}
            invoice_content['invoice_date_due'] = inv.invoice_date_due.strftime(
                '%d/%m/%Y')
            invoice_content['l10n_bo_cuf'] = inv.l10n_bo_cuf
            invoice_content['l10n_bo_invoice_number'] = inv.l10n_bo_invoice_number
            invoice_content['client_vat'] = inv.partner_id.vat
            invoice_content['client_name'] = inv.partner_id.name
            invoice_content['amount_total'] = inv.amount_total
            invoice_content['amount_by_group'] = inv.amount_by_group
            invoice_content['amount_untaxed'] = inv.amount_untaxed
            data[index] = invoice_content

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'sales.book.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # Cell Format
        sheet = workbook.add_worksheet()
        sheet.set_column('A:X', 25)
        cell_format = workbook.add_format({'font_size': '12px'})
        title = workbook.add_format(
            {'align': 'left', 'bold': True, 'font_size': '16px'})
        title.set_font_color('blue')
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '12px'})
        head.set_pattern(2)
        head.set_bg_color('blue')
        head.set_font_color('white')
        txt = workbook.add_format({'font_size': '10px'})
        # Headers
        sheet.merge_range('A1:D2', 'Registro de Ventas Estandar', title)
        sheet.merge_range('A3:B3', '(Expresado en Bolivianos)', txt)
        sheet.write('A4', 'N°', head)
        sheet.write('B4', 'Especificación', head)
        sheet.write('C4', 'Fecha de la Factura', head)
        sheet.write('D4', 'N° de la Factura', head)
        sheet.write('E4', 'Código de Autorización', head)
        sheet.write('F4', 'NIT/CI Cliente', head)
        sheet.write('G4', 'Complemento', head)
        sheet.write('H4', 'Nombre o Razón Social', head)
        sheet.write('I4', 'Importe Total de la Venta', head)
        sheet.write('J4', 'Importe ICE', head)
        sheet.write('K4', 'Importe IEHD', head)
        sheet.write('L4', 'Importe IPJ', head)
        sheet.write('M4', 'Tasas', head)
        sheet.write('N4', 'Otros No Sujetos al IVA', head)
        sheet.write('O4', 'Exportaciones y Operaciones Exentas', head)
        sheet.write('P4', 'Ventas Gravadas a Tasa Cero', head)
        sheet.write('Q4', 'Subtotal', head)
        sheet.write(
            'R4', 'Descuentos, Bonificaciones y Rebajas Sujetas al IVA', head)
        sheet.write('S4', 'Importe Gift Card', head)
        sheet.write('T4', 'Importe Base para Débito Fiscal', head)
        sheet.write('U4', 'Debito Fiscal', head)
        sheet.write('V4', 'Estado', head)
        sheet.write('W4', 'Código de Control', head)
        sheet.write('X4', 'Tipo de Venta', head)
        # Data Iteration
        for index, inv in enumerate(data.items()):
            # print(index % 2)
            # if(index % 2 == 0):
            #     print('entra')
            #     txt.set_bg_color('#97c5db')
            print(inv[1]['amount_by_group'])
            sheet.write('A' + str(int(inv[0]) + 5), str(int(inv[0]) + 1), txt)
            sheet.write('B' + str(int(inv[0]) + 5), '2', txt)
            sheet.write('C' + str(int(inv[0]) + 5),
                        inv[1]['invoice_date_due'], txt)
            sheet.write('D' + str(int(inv[0]) + 5),
                        inv[1]['l10n_bo_invoice_number'], txt)
            sheet.write('E' + str(int(inv[0]) + 5), inv[1]['l10n_bo_cuf'], txt)
            sheet.write('F' + str(int(inv[0]) + 5), inv[1]['client_vat'], txt)
            sheet.write('G' + str(int(inv[0]) + 5), '', txt)
            sheet.write('H' + str(int(inv[0]) + 5), inv[1]['client_name'], txt)
            sheet.write('I' + str(int(inv[0]) + 5),
                        inv[1]['amount_total'], txt)
            sheet.write('J' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('K' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('L' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('M' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('N' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('O' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('P' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('Q' + str(int(inv[0]) + 5),
                        inv[1]['amount_total'], txt)
            # sheet.write('R' + str(int(inv[0]) + 5),
            #             inv[1]['amount_by_group'], txt)
            sheet.write('R' + str(int(inv[0]) + 5), '0', txt)
            sheet.write('S' + str(int(inv[0]) + 5), '0.00', txt)
            sheet.write('T' + str(int(inv[0]) + 5),
                        inv[1]['amount_untaxed'], txt)
            deb_fiscal = (int(inv[1]['amount_untaxed'])
                          * 0.13)
            sheet.write('U' + str(int(inv[0]) + 5),
                        str(round(deb_fiscal, 2)), txt)
            sheet.write('V' + str(int(inv[0]) + 5), 'V', txt)
            sheet.write('W' + str(int(inv[0]) + 5), '0', txt)
            sheet.write('X' + str(int(inv[0]) + 5), '0', txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
