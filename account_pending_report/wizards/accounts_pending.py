# -*- coding: utf-8 -*-
import io
import base64
import datetime
from odoo.tools.misc import xlwt
from odoo.tools import date_utils
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from xlsxwriter.utility import xl_rowcol_to_cell


class WizardClassName(models.TransientModel):
    _name = 'account.pending.report'

    nature = fields.Selection([
        ('payable',_("Por Pagar")),
        ('receivable',_("Por Cobrar"))
    ], default="receivable", string="Tipo de Reporte")

    dt_initial = fields.Date(string=_("Initial Date"))
    dt_final = fields.Date(string=_("Final Date"))

    # Function button
    def print_XLSX(self):
        data = {
			'ids': self.ids,
			'model': self._name,
            'nature': self.nature,
			'wizard': {
                'nature': self.nature
            }
        }
        return self.env.ref('account_pending_report.ikatech_report_xlsx').report_action(self, data=data)


class ReportAccountPendingXlsx(models.AbstractModel):
    _name = 'report.account_pending_report.accpend_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        header = workbook.add_format({'font_size': 12, 'font_color':'#FFFFFF', 'bg_color':'#8B46CD','bold':True, 'align':'center', 'valign':'vcenter'})
        subheaders = workbook.add_format({'font_size': 11, 'font_color':'#FFFFFF', 'bg_color':'#E75CE0','bold':True, 'align':'center', 'valign':'vcenter'})
        subtitles_h3 = workbook.add_format({'font_size': 12, 'bg_color':'#FFCC6D','bold':True, 'align':'right'})
        subtitles = workbook.add_format({'font_size': 10, 'bg_color':'#FFCC6D','bold':True, 'align':'center'})
        text_number = workbook.add_format({'font_size': 10,  'align':'right'})
        text_number.set_num_format('$#,##0.00')
        text_partners = workbook.add_format({'font_size': 10, 'bold':True, 'align':'right'})
        style_sumtot = workbook.add_format({'font_size': 10, 'bg_color':'#FFCC6D','bold':True, 'align':'right'})
        style_sumtot.set_num_format('$#,##0.00')
        title = 'Cuentas Por Cobrar Pendientes' if records['nature'] == 'receivable' else 'Cuentas Por Pagar Pendientes'

        sheet = workbook.add_worksheet(title)
        # sheet.hide_gridlines(2)
        current_datetime = fields.Datetime.context_timestamp(self, fields.Datetime.now()) # Get current day to get numbers of months
        number_months = current_datetime.month
        sheet.set_row(2, 25) #set height in row number 3
        sheet.set_column('B:C',30)
        sheet.merge_range(2, 2, 1, int(number_months + 14), title, header)
        concept = "CLIENTES"  if records['nature'] == 'receivable' else "PROVEEDORES"
        sheet.merge_range(5,1, 5, 2, concept, subtitles) #(first_row, first_col, last_row, last_col, data, cell_format])

        row_initial, column_initial = 5, 3
        row_position = row_initial
        column_position = column_initial

        # we set month headers
        for month in range(number_months):
            sheet.set_column(column_position,column_position, 20) #set width cell to 20
            # sheet.write(row, col, data, style). star in cell D5
            sheet.write(row_position, column_position, self.convert_monht(month), subheaders)
            column_position += 1
        #* Antes de reiniciar la columnas establecer los rangos de cuentas antiguas.
        col_ageing = number_months + 3 # Espaciado
        sheet.set_column(col_ageing,col_ageing, 5)
        sheet.write(row_position-1, col_ageing+1, self.convert_monht(number_months -1), subtitles)
        sheet.write(row_position, col_ageing+1, "Corriente", subheaders)
        sheet.write(row_position-1, col_ageing+2, self.convert_monht(number_months -2), subtitles)
        sheet.write(row_position, col_ageing+2, "Días 1-30", subheaders)
        sheet.write(row_position-1, col_ageing+3, self.convert_monht(number_months -3), subtitles)
        sheet.write(row_position, col_ageing+3, "Días 31-60", subheaders)
        sheet.write(row_position-1, col_ageing+4, self.convert_monht(number_months -4), subtitles)
        sheet.write(row_position, col_ageing+4, "Días 61-90", subheaders)
        # another style
         #xl_rowcol_to_cell(row, col)
        sheet.merge_range(row_position-1, col_ageing+5, row_position, col_ageing+5, 'Más de 90 Días', subheaders)
        sheet.merge_range(row_position-1, col_ageing+6, row_position, col_ageing+6, '2do Semestre Año Anterior', subheaders)
        sheet.set_column(col_ageing+6,col_ageing+7, 30) #Ajust width for columns semester
        sheet.merge_range(row_position-1, col_ageing+7, row_position, col_ageing+7, '1er Semestre Año Anterior', subheaders)
        sheet.merge_range(row_position-1, col_ageing+8, row_position, col_ageing+8, 'Año Anterior', subheaders)
        sheet.merge_range(row_position-1, col_ageing+9, row_position, col_ageing+9, 'Años Anteriores', subheaders)
        sheet.set_column(col_ageing+1,col_ageing+9, 20)
        # * End
        row_position += 1 #row jump
        column_position = column_initial # reset columns position
        args = {
            'number_months': number_months,
            'current_datetime': current_datetime,
            'sheet': sheet,
            'row_initial': row_initial,
            'column_initial': column_initial,
            'column_position':column_position,
            'col_ageing': col_ageing,
            'text_number': text_number,
            'subtitles': subtitles,
            'text_partners': text_partners,
            'style_sumtot': style_sumtot
        }
        #?Group 1
        if records['nature'] == 'receivable':
            accounts = tuple(self.env['account.account'].search([('code','=ilike','1100010%')]).ids)
        else:
            accounts = tuple(self.env['account.account'].search([('code','=ilike','20000%')]).ids)
        row_position = self.calculate_data(accounts, row_position, concept, args)

        sheet.merge_range(row_position,1, row_position+1, int(number_months + 14), "")

        #?Group 2
        row_position += 2 #row debtors
        # merge_range(first_row, first_col, last_row, last_col, data, cell_format])
        concept = "DEUDORES VARIOS"  if records['nature'] == 'receivable' else "ACREEDORES VARIOS"
        sheet.merge_range(row_position,1, row_position, 2, concept, subtitles)
        row_position += 1 #row jump
        if records['nature'] == 'receivable':
            accounts = tuple(self.env['account.account'].search( ['|', ('code','=ilike','115%'), ('code','=ilike','120%'), '!', ('code', 'in', ('12040001','12040002'))]).ids)
        else:
            accounts = tuple(self.env['account.account'].search([('code','=ilike','20010%')]).ids)
        row_position = self.calculate_data(accounts, row_position, concept, args)

        sheet.merge_range(row_position,1, row_position+1, int(number_months + 14), "")

        #?Group 3
        row_position += 2 #row debtors
        concept = "CUENTAS POR COBRAR EMPRESAS RELACIONADAS"  if records['nature'] == 'receivable' else "CUENTAS POR PAGAR EMPRESAS RELACIONADAS"
        sheet.merge_range(row_position,1, row_position, 2, concept, subtitles)
        row_position += 1 #row jump
        if records['nature'] == 'receivable':
            accounts = tuple(self.env['account.account'].search([('code','=ilike','12510%')]).ids)
        else:
            accounts = tuple(self.env['account.account'].search([('code','=ilike','22510%')]).ids)
        row_position = self.calculate_data(accounts, row_position, concept, args)

        sheet.merge_range(row_position,1, row_position+1, int(number_months + 14), "")

        #?Group 4
        row_position += 2 #row debtors
        concept = "CUENTAS POR COBRAR EMPRESAS RELACIONADAS LP"  if records['nature'] == 'receivable' else "CUENTAS POR PAGAR EMPRESAS RELACIONADAS LP"
        sheet.merge_range(row_position,1, row_position, 2, concept, subtitles)
        row_position += 1 #row jump
        if records['nature'] == 'receivable':
            accounts = tuple(self.env['account.account'].search([('code','=ilike','17010%')]).ids)
        else:
            accounts = tuple(self.env['account.account'].search([('code','=ilike','27010%')]).ids)
        row_position = self.calculate_data(accounts, row_position, concept, args)


    def calculate_data(self, accounts, row_position, concept, args):
        # start calculation by partner
        start_position = row_position
        self.env.cr.execute("SELECT id, name FROM res_partner WHERE active=true ORDER BY id")
        dic_partners = self.env.cr.dictfetchall()
        for partner in dic_partners: # iterate partner by partner
            columns_months, exist_move = args['column_position'], True
            for month in range(args['number_months']): #check month by month
                sql_balance = """SELECT SUM(debit) - SUM(credit) AS balance FROM account_move_line WHERE partner_id = {} AND account_id in {}
                    AND EXTRACT(YEAR FROM date) <= {} AND EXTRACT(MONTH FROM date) <= {} AND parent_state = 'posted'""".format(partner['id'], accounts, args['current_datetime'].year, month + 1)
                self.env.cr.execute(sql_balance)
                balance = self.env.cr.dictfetchall()
                if balance[0]['balance'] != 0 and balance[0]['balance'] != None: # only print movements with balance
                    if exist_move: # Print partner for first time, then, change flag
                        args['sheet'].merge_range("B{0}:C{0}".format(row_position+1),  partner['name'], args['text_partners'])
                        exist_move = False
                    args['sheet'].write(row_position, columns_months, balance[0]['balance'], args['text_number'])
                columns_months += 1 # jump to another month
            if not exist_move:
                 #-start calculating by periods
                self.calculate_ageing(partner, row_position, args['col_ageing'], args['sheet'], args['text_number'], accounts)
                #-end calculating by periods
                row_position += 1 #if not exist movement with the partner, don't jump row
        last_row_g1 = row_position #Save last position for formulas
        row_position += 1 #row jump
        columns_months = args['column_initial'] # reset columns position
        args['sheet'].merge_range("B{0}:C{0}".format(row_position),  "TOTAL {}".format(concept), args['subtitles'])
        for month in range(args['number_months'] + 10):# formulas are added to add totals per month
            #xl_rowcol_to_cell(row, col)
            if month == int(args['number_months']): #empty middle column
                columns_months += 1
                continue
            cell_init = xl_rowcol_to_cell(start_position, columns_months) #initial cell by month
            cell_end = xl_rowcol_to_cell(last_row_g1 -1, columns_months) # ending cell by month
            args['sheet'].write_formula(row_position -1, columns_months, "=SUM({}:{})".format(cell_init, cell_end), args['style_sumtot']) #added formula
            columns_months += 1 #jump column (month)
        return row_position

    #start calculating by periods
    def calculate_ageing(self, partner, row, col, sheet, text_number, accounts):
        query = """ SELECT SUM(amount_residual) AS amount_residual FROM account_move_line WHERE
            parent_state = 'posted' AND partner_id = {} AND
            account_id IN {} AND full_reconcile_id IS NULL """.format(partner['id'], accounts)
        #Current month
        self.fill_row_group(0, "", sheet, query, row, col + 1, text_number)
        # First Month
        self.fill_row_group(1, "", sheet, query, row, col + 2, text_number)
        # Second Month
        self.fill_row_group(2, "", sheet, query, row, col + 3, text_number)
        # Third  Month
        self.fill_row_group(3, "", sheet, query, row, col + 4, text_number)
        # fourth  Month or after
        self.fill_row_group(4, "year", sheet, query, row, col + 5, text_number)
        # Second Semester year before
        # First Semester year before
        # 2 years before
        #Last Years
        #Total

    def fill_row_group(self, month, closer, sheet, query, row, col, text_number):
        current_date = fields.Date.context_today(self)
        if closer == "":
            query_dates = "AND EXTRACT(MONTH FROM DATE) ={} ".format(current_date.month - month)
        elif closer == "year":
             query_dates = "AND EXTRACT(MONTH FROM DATE) <={}".format(current_date.month - month)
        self.env.cr.execute(query + query_dates)
        ar = self.env.cr.dictfetchall()[0]
        sheet.write(row, col, ar['amount_residual'], text_number)

    def convert_monht(self, number):
        months = [
            'Enero',
            'Febrero',
            'Marzo',
            'Abril',
            'Mayo',
            'Junio',
            'julio',
            'Agosto',
            'Septiembre',
            'Octubre',
            'Noviembre',
            'Diciembre',
            ]
        return months[int(number)]
