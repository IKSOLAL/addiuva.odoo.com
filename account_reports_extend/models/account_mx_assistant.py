# -*- coding: utf-8 -*-

from odoo import models, api, fields
from datetime import datetime

class AccountReportAssistant(models.TransientModel):
    _name = 'account.report.assistant'
    
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    num_order = fields.Char(string="Numero de orden")
    
    def print_report_xml(self):
        # event = self.env['account.move.line'].search_read([('date','>=',self.start_date),('date','<=',self.end_date)])
        data = {   
            'start_date': self.start_date,
            'end_date': self.end_date,
            'num_order': self.num_order
        }
        return self.env.ref('account_reports_extend.account_xml_assistant').report_action(self, data=data)
    
    
class AccountMoveAssistantXmlReport(models.TransientModel):
    _name = "report.account_reports_extend.report_move_assis"
    _inherit = 'report.report_xml.abstract'
    
    def validate_report(self, xsd_schema_doc, content):
        return
    
    @api.model
    def _get_report_values(self, docids, data=None):
        start_date = data['start_date']
        end_date = data['end_date']
        num_order = data['num_order']
        company_id = self.env.company
        cr = self._cr
        # Get accounts
        # Las cuentas de tipo [Ingresos, Otros Ingresos, Costo de Ingresos, Gastos, Otros Gastos, Depreciación, Hoja Fuera de Balance] sus saldos iniciales a inciios de año se deben setear a cero.
        # Para esto usamnos el campo include_initial_balance de account_account_type, si esta como false o null los saldos iniciales no seran incluidos y seran seteados en cero
        account_query = """ SELECT aa.id, aa.code, aa.name, aat.include_initial_balance FROM account_account aa 
            INNER JOIN account_account_type aat ON (aa.user_type_id = aat.id)
            WHERE aa.deprecated = false AND aa.company_id = {} ORDER BY aa.code; 
            """.format(company_id.id)
        cr.execute(account_query)
        accounts = cr.dictfetchall()
        # {'id': 91585, 'code': '89901001', 'name': 'Contra orden'}
        detail_data = []
        for account in accounts:
            # if account['include_initial_balance'] in (False, None):
                # setear en cero en cambio de año fiscal. fecha de inicio cambiar
                #  initial_balance_date = str(datetime.strftime(datetime.strptime(start_date, "%Y-%m-%d"), "%Y")) + '-01-01'
                #  where_date = """ date >= AND date <=  """.format(initial_balance_date, start_date)
            if account['include_initial_balance'] in (False, None):
                initial_balance_date = str(datetime.strftime(datetime.strptime(start_date, "%Y-%m-%d"), "%Y")) + '-01-01'
                with_balance = "date >= '{}'::DATE AND date < '{}'::DATE ".format(initial_balance_date, start_date)
            else:
                with_balance = "date < '{}'::DATE ".format(start_date)
            query = """ SELECT CAST(SUM(debit) AS varchar) debit, CAST(SUM(credit) AS varchar) credit, CAST(SUM(debit - credit) AS varchar) balance 
                FROM account_move_line WHERE account_id = {} AND {}
                AND parent_state='posted' AND company_id = {}""".format(account['id'], with_balance, company_id.id)
            cr.execute(query)
            data = cr.dictfetchall()
            if str(datetime.strftime(datetime.strptime(start_date, "%Y-%m-%d"), "%m")) == '01':  
                if account['include_initial_balance'] in (False, None):
                    print(account['code'] + " " +account['name'])
                    data[0]['balance'] = 0
            balance_start, balance_end = self.calculate_balance_end(start_date, end_date, account['id'], data[0]['balance'], company_id.id)
            data[0]['balance'] = str(balance_start)
            data[0]['balance_end'] = str(balance_end)
            data[0]['account_id'] = account['id']
            data[0]['code'] = account['code']
            data[0]['name'] = account['name']
            # [{'debit': 4553531.09, 'credit': 5031784.31, 'balance': -478253.22, 'account_id': 40640, 'code': '24000055', 'name': 'Retenciones ISR 2%'}]
            detail_query = """ SELECT CAST(aml.debit AS varchar), CAST(aml.credit AS varchar), am.name AS folio, aml.date, aml.name AS tag  
            FROM account_move_line aml INNER JOIN account_move am ON (aml.move_id = am.id) 
            WHERE aml.account_id = {} AND
            aml.date >= '{}'::DATE AND aml.date <= '{}'::DATE  AND aml.company_id = {} AND aml.parent_state = 'posted'
            ORDER BY aml.date""".format(account['id'], start_date, end_date, company_id.id)
            # detail_query = """ SELECT CAST(debit AS varchar), CAST(credit AS varchar), move_name AS folio, date, name AS tag  
            # FROM account_move_line WHERE account_id = {} AND
            # date >= '{}'::DATE AND date <= '{}'::DATE  AND company_id = {}
            # ORDER BY date""".format(account['id'], start_date, end_date, company_id.id)
            cr.execute(detail_query)
            move_lines = cr.dictfetchall()
            if move_lines:
                data[0]['lines'] = move_lines
                detail_data.append(data[0])
                
        general_data = {
            'rfc_company': company_id.vat,
            'year': datetime.strftime(datetime.strptime(start_date, "%Y-%m-%d"), "%Y"),
            'month': datetime.strftime(datetime.strptime(start_date, "%Y-%m-%d"), "%m"),
            'type': 'AF',
            'order': num_order,
        }
        
        data = {
            'general': general_data,
            'start_date': start_date, 
            'end_date': end_date, 
            'data': detail_data,
        }
        
        
        return data
    
    
    def calculate_balance_end(self, dt_start, dt_end, account_id, initial_balance, company_id):
        query = """ SELECT SUM(debit) AS debit, SUM(credit) AS credit, SUM(debit - credit) AS balance_end 
            FROM account_move_line WHERE account_id = {} AND
            date >= '{}'::DATE AND date <= '{}'::DATE AND parent_state='posted' AND company_id = {}""".format(account_id, dt_start, dt_end, company_id)
        self._cr.execute(query)
        bl = self._cr.dictfetchall()
        # print("initial_balance : ", initial_balance)
        # print("balance_end : ",  bl[0]['balance_end'])
        ib = float(initial_balance) if initial_balance != None else 0
        bend = float(bl[0]['balance_end']) if bl[0]['balance_end'] != None else 0
        eb = ib + bend
        # print("b + bend : ", eb)
        return ib, eb