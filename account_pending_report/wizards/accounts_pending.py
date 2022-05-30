# -*- coding: utf-8 -*-
import io
import base64
import datetime
import calendar
from dateutil.relativedelta import relativedelta
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

    detail = fields.Boolean(default=True, string="Detallado")
    
    dt_initial = fields.Date(string=_("Initial Date"))
    dt_final = fields.Date(string=_("Final Date"))

    # Function button
    def print_XLSX(self):
        data = {
			'ids': self.ids,
			'model': self._name,
            'nature': self.nature,
            'detail': self.detail,
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
        text_number = workbook.add_format({'font_size': 8, 'align':'right', 'font_color':'#6e6e6e'})
        text_number.set_num_format('$#,##0.00')
        sum_group = workbook.add_format({'font_size': 10,  'align':'right', 'bg_color':'#dbdbdb', 'bold':True})
        sum_group.set_num_format('$#,##0.00')
        text_partners = workbook.add_format({'font_size': 10, 'bold':True, 'align':'right', 'bg_color':'#dbdbdb'})
        text_accounts = workbook.add_format({'font_size': 8, 'align':'right', 'font_color':'#6e6e6e'})
        style_sumtot = workbook.add_format({'font_size': 10, 'bg_color':'#FFCC6D','bold':True, 'align':'right'})
        style_sumtot.set_num_format('$#,##0.00')
        stl_totv = workbook.add_format({'font_size': 10, 'bg_color':'#dbdbdb','bold':True, 'align':'right'})
        stl_totv.set_num_format('$#,##0.00')

        title = 'Cuentas Por Cobrar Pendientes' if records['nature'] == 'receivable' else 'Cuentas Por Pagar Pendientes'
        
        sheet = workbook.add_worksheet(title)
        sheet.hide_gridlines(2)
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
        current_year = current_datetime.year
        
        # we set month headers
        for month in range(number_months):
            year_cmonth = self.current_year(month)
            sheet.set_column(column_position,column_position, 20) #set width cell to 20
            # sheet.write(row, col, data, style). star in cell D5
            sheet.write(row_position, column_position, self.convert_monht(month), subheaders)
            column_position += 1
        # create row mention year
        sheet.merge_range(4,3, 4, column_position -1, str(current_year), subtitles) #(first_row, first_col, last_row, last_col, data, cell_format])
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
        sheet.merge_range(row_position-1, col_ageing+10, row_position, col_ageing+10, 'Total', subheaders) 
        sheet.set_column(col_ageing+1,col_ageing+10, 20)
        # sheet.set_column(col_ageing+10,col_ageing+10, 2)
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
            'style_sumtot': style_sumtot,
            'text_accounts': text_accounts,
            'sum_group': sum_group,
            'stl_totv':stl_totv
        }
        #?Group 1
        if records['nature'] == 'receivable':
            accounts = tuple(self.env['account.account'].search([('code','=ilike','1100010%')]).ids)
        else:
            accounts = tuple(self.env['account.account'].search([('code','=ilike','20000%')]).ids)
        row_position = self.calculate_data(accounts, row_position, concept, args, records['detail'])
        
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
        row_position = self.calculate_data(accounts, row_position, concept, args, records['detail'])
        
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
        row_position = self.calculate_data(accounts, row_position, concept, args, records['detail'])

        sheet.merge_range(row_position,1, row_position+1, int(number_months + 14), "")

        #?Group 4
        row_position += 2 #row debtors
        concept = "CUENTAS POR COBRAR EMPRESAS RELACIONADAS LP"  if records['nature'] == 'receivable' else "CUENTAS POR PAGAR EMPRESAS VINCULADAS"
        sheet.merge_range(row_position,1, row_position, 2, concept, subtitles) 
        row_position += 1 #row jump
        if records['nature'] == 'receivable':
            accounts = tuple(self.env['account.account'].search([('code','=ilike','17010%')]).ids)
        else:
            accounts = tuple(self.env['account.account'].search([('code','=ilike','27010%')]).ids)
        row_position = self.calculate_data(accounts, row_position, concept, args, records['detail'])


    def calculate_data(self, accounts, row_position, concept, args, detail):
        start_position = row_position
        self.env.cr.execute("""SELECT aml.partner_id AS id, rp.name, SUM(aml.debit - aml.credit) AS balance FROM account_move_line aml 
        INNER JOIN res_partner rp ON (aml.partner_id = rp.id) 
        WHERE aml.account_id in {} AND aml.parent_state = 'posted' GROUP BY aml.partner_id,  rp.name""".format(accounts))
        dic_partners = self.env.cr.dictfetchall() 
        for partner in dic_partners:
            if partner['balance'] == 0: continue
            columns_months = args['column_position']
            args['sheet'].merge_range("B{0}:C{0}".format(row_position+1),  partner['name'], args['text_partners']) #- establece nombre
            for month in range(args['number_months']):
                sql_balance = """SELECT  SUM(debit - credit) AS balance FROM account_move_line WHERE partner_id = {} AND account_id in {} 
                    AND EXTRACT(YEAR FROM date) <= {} AND EXTRACT(MONTH FROM date) <= {} AND parent_state = 'posted'""".format(partner['id'], accounts, args['current_datetime'].year, month + 1)
                self.env.cr.execute(sql_balance)
                balance = self.env.cr.dictfetchall()
                args['sheet'].write(row_position, columns_months, balance[0]['balance'], args['sum_group'])
                columns_months += 1 # jump to another month
            self.calculate_ageing(partner, row_position, args['col_ageing'], args['sheet'], args['text_number'], accounts, "partner", args['sum_group'], args['stl_totv'], 'partner')
            if detail:
                for account in accounts: #- itera por cuentas
                    exist_move, columns_months = True, args['column_position']
                    for month in range(args['number_months']): #check month by month
                        sql_balance = """SELECT aml.account_id, CONCAT(aa.code, ' ', aa.name) AS name_account,  SUM(aml.debit - aml.credit) AS balance FROM account_move_line aml 
                        INNER JOIN account_account aa ON (aml.account_id = aa.id)
                        WHERE aml.partner_id = {} AND aml.account_id = {} 
                        AND EXTRACT(YEAR FROM aml.date) <= {} AND EXTRACT(MONTH FROM aml.date) <= {} AND aml.parent_state = 'posted'  GROUP BY aml.account_id, name_account """.format(partner['id'], account, args['current_datetime'].year, month + 1)
                        self.env.cr.execute(sql_balance)
                        balance = self.env.cr.dictfetchall()
                        if balance:
                            if balance[0]['balance'] != 0 and balance[0]['balance'] != None: # only print movements with balance
                                if exist_move: # Print partner for first time, then, change flag
                                    row_position += 1 #row jump
                                    args['sheet'].merge_range("B{0}:C{0}".format(row_position + 1),  balance[0]['name_account'], args['text_accounts']) 
                                    exist_move = False
                                args['sheet'].write(row_position , columns_months, balance[0]['balance'], args['text_number'])
                        columns_months += 1 # jump to another month
                    if not exist_move: 
                        #-start calculating by periods
                        self.calculate_ageing(partner, row_position, args['col_ageing'], args['sheet'], args['text_number'], account, "accounts", args['sum_group'], args['stl_totv'],'accounts')
                        #-end calculating by periods
                row_position += 1 #row jump
        last_row_g1 = row_position #Save last position for formulas
        row_position += 1 #row jump
        columns_months = args['column_initial'] # reset columns position
        args['sheet'].merge_range("B{0}:C{0}".format(row_position),  "TOTAL {}".format(concept), args['subtitles'])
        for month in range(args['number_months'] + 11):# formulas are added to add totals per month
            #xl_rowcol_to_cell(row, col)
            if month == int(args['number_months']): #empty middle column
                columns_months += 1
                continue
            cell_init = xl_rowcol_to_cell(start_position, columns_months) #initial cell by month
            cell_end = xl_rowcol_to_cell(last_row_g1 -1, columns_months) # ending cell by month
            args['sheet'].write_formula(row_position -1, columns_months, "=SUM({}:{})/2".format(cell_init, cell_end), args['style_sumtot']) #added formula
            columns_months += 1 #jump column (month)
        return row_position


    def calculate_ageing(self, partner, row, col, sheet, text_number, account, type_sum, sum_group, stl_totv, type_opt):
        query = """ SELECT SUM(amount_residual) AS amount_residual FROM account_move_line WHERE 
                parent_state = 'posted' AND partner_id = {} AND full_reconcile_id IS NULL """.format(partner['id'])
        if type_sum == "accounts":
            query = query +  " AND  account_id = {}  ".format(account)
        else:
            query = query +  " AND  account_id in {}  ".format(account)
        #Current month
        self.fill_row_group(0, "", sheet, query, row, col + 1, text_number, sum_group, type_sum)
        # First Month
        self.fill_row_group(1, "", sheet, query, row, col + 2, text_number, sum_group, type_sum)
        # Second Month
        self.fill_row_group(2, "", sheet, query, row, col + 3, text_number, sum_group, type_sum)
        # Third  Month
        self.fill_row_group(3, "", sheet, query, row, col + 4, text_number, sum_group, type_sum)
        # fourth  Month or after
        self.fill_row_group(4, "+90", sheet, query, row, col + 5, text_number, sum_group, type_sum)
        # Second Semester year before
        self.fill_row_group(7,  "2s", sheet, query, row, col + 6, text_number, sum_group, type_sum)
        # First Semester year before
        self.fill_row_group(6,  "1s", sheet, query, row, col + 7, text_number, sum_group, type_sum)
        # 2 years before
        self.fill_row_group(0,  "2y", sheet, query, row, col + 8, text_number, sum_group, type_sum)
        #Last Years
        self.fill_row_group(0,  "3y", sheet, query, row, col + 9, text_number, sum_group, type_sum)
        #Total
        cell_init = xl_rowcol_to_cell(row ,  col + 1) #initial cell by month
        cell_end = xl_rowcol_to_cell(row , col + 9) # ending cell by month
        style = stl_totv if type_opt == 'partner' else text_number
        sheet.write_formula(row, col + 10 , "=SUM({}:{})".format(cell_init, cell_end), style) #added formula

    def fill_row_group(self, month, closer, sheet, query, row, col, text_number, sum_group, type_sum):
        current_date = fields.Date.context_today(self)
        if closer == "":
            date_group = current_date - relativedelta(months=month)
            if current_date.year != date_group.year: return False
            query_dates = "AND EXTRACT(MONTH FROM DATE) ={} AND EXTRACT(YEAR FROM date) = {} ".format(current_date.month - month, date_group.year)
        elif closer == "+90":
            date_group = current_date - relativedelta(months=month)
            if current_date.year != date_group.year: return False
            query_dates = "AND EXTRACT(MONTH FROM DATE) <={} AND EXTRACT(YEAR FROM date) = {} ".format(current_date.month - month, date_group.year)
        elif closer == "2s":
            date_group = current_date - relativedelta(year=1)
            query_dates = "AND EXTRACT(MONTH FROM DATE) >={} AND EXTRACT(YEAR FROM date) = {} ".format(month, date_group.year)
        elif closer == "1s":
            date_group = current_date - relativedelta(year=1)
            query_dates = "AND EXTRACT(MONTH FROM DATE) <={} AND EXTRACT(YEAR FROM date) = {} ".format(month, date_group.year)
        elif closer == "2y":
            date_group = current_date - relativedelta(year=2)
            query_dates = "AND EXTRACT(YEAR FROM DATE) = {}".format(date_group.year)
        elif closer == "3y":
            date_group = current_date - relativedelta(year=3)
            query_dates = "AND EXTRACT(YEAR FROM DATE) <= {}".format(date_group.year)
        self.env.cr.execute(query + query_dates)
        ar = self.env.cr.dictfetchall()[0] 
        style = text_number if type_sum == "accounts" else sum_group
        sheet.write(row, col, ar['amount_residual'], style)
        
    
    def current_year(self, num_month):
        current_date = fields.Date.context_today(self)
        date = current_date - relativedelta(months=num_month)
        return date.year
    
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