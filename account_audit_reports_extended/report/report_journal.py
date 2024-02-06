# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models


class ReportJournalExcel(models.Model):
    _name = "report.accounting_excel_reports.report_journal_excel"
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Journal Excel'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.account.report_journal']
        result = report_obj._get_report_values(obj, data)
        res_company = self.env.user.company_id

        for o in result['docs']:
            sheet = workbook.add_worksheet()

            format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                           'align': 'center', 'bold': True, 'bg_color': '#bfbfbf', 'valign': 'vcenter'})
            format2 = workbook.add_format({'font_size': 12, 'align': 'left', 'right': True, 'left': True,
                                           'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
            format3 = workbook.add_format({'font_size': 12, 'align': 'right', 'right': True, 'left': True,
                                           'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
            format4 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': True, 'right': True, 'left': True,
                                           'bottom': True, 'top': True})
            format5 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': True, 'right': True, 'left': True,
                                           'bottom': True, 'top': True})
            format6 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                           'bottom': True, 'top': True})
            format7 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': False, 'right': True,
                                           'left': True, 'bottom': True, 'top': True})
            format8 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True,
                                           'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})

            if data['form']['amount_currency']:
                last_col = 7
                sheet.merge_range('A1:H1', "Journal Audit Report", format1)
            else:
                last_col = 6
                sheet.merge_range('A1:G1', "Journal Audit Report", format1)

            sheet.set_row(0, 40)
            sheet.set_column(0, last_col, 25)

            row = 2
            sheet.write('A3', "Company", format4)
            sheet.write('B3', res_company.name, format6)
            sheet.write(row, last_col-1, "Journal", format4)
            sheet.write(row, last_col, o.name, format6)
            sheet.write('A4', "Entries Sorted by", format4)
            if data['form'].get('sort_selection') != 'l.date':
                sheet.write('B4', "Journal Entry Number", format6)
            else:
                sheet.write('B4', "Date", format6)
            sheet.write(row+1, last_col-1, "Target Moves", format4)
            if data['form']['target_move'] == 'posted':
                sheet.write(row+1, last_col, "All Posted Entries", format6)
            else:
                sheet.write(row+1, last_col, "All Entries", format6)

            sheet.write('A6', "Move ", format2)
            sheet.write('B6', "Date", format2)
            sheet.write('C6', "Account", format2)
            sheet.write('D6', "Partner", format2)
            sheet.write('E6', "Label", format2)
            sheet.write('F6', "Debit", format3)
            sheet.write('G6', "Credit", format3)
            if data['form']['amount_currency']:
                sheet.write('H6', "Currency", format2)
            row = 7
            col = 0
            for aml in result['lines'][o.id]:
                sheet.write(row, col, aml.move_id.name != '/' and aml.move_id.name or ('*'+str(aml.move_id.id)), format6)
                sheet.write(row, col+1, aml.date, format6)
                sheet.write(row, col+2, aml.account_id.code, format6)
                sheet.write(row, col+3, aml.sudo().partner_id and aml.sudo().partner_id.name and aml.sudo().partner_id.name[:23] or '', format6)
                sheet.write(row, col+4, aml.name and aml.name[:35], format6)
                sheet.write(row, col+5, aml.debit, format7)
                sheet.write(row, col+6, aml.credit, format7)
                if data['form']['amount_currency']:
                    sheet.write(row, col+7, aml.amount_currency or 0.0, format6)
                row += 1
            sheet.merge_range(row, col, row, col+4, "Total", format4)
            sheet.write(row, col+5, result['sum_debit'](data, o), format5)
            sheet.write(row, col+6, result['sum_credit'](data, o), format5)
            row += 3
            sheet.merge_range(row, col, row, col+2, "Tax Declaration", format8)
            row += 1
            sheet.write(row, col, "Name", format4)
            sheet.write(row, col+1, "Base Amount", format4)
            sheet.write(row, col+2, "Tax Amount", format4)
            row += 1
            taxes = result['get_taxes'](data, o)
            for tax in taxes:
                sheet.write(row, col, tax.name, format6)
                sheet.write(row, col+1, taxes[tax]['base_amount'], format7)
                sheet.write(row, col+2, taxes[tax]['tax_amount'], format7)
