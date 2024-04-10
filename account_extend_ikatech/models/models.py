# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class account_reports_pandl(models.TransientModel):
    _name = 'account.reports.pandl'

    name = fields.Char()
    date_from = fields.Datetime(string=_("Date From"))
    date_to = fields.Datetime(string=_("Date to"))
    company_id = fields.Many2one('res.company', string='Company',  default=lambda self: self.env.company)
    
    @api.model
    def pandl_report(self, option):
        data_report = {}
        # report_values = self.env['account.reports.pandl'].search(
        #     [('id', '=', option[0])])
        dates, date_names = [],[]
        comparation = option[3]
        months_n = option[4]
        date_names.append('Del {} Al {}'.format(option[2].get('date_to'), option[2].get('date_from')))
        if comparation: # Si hay que comparar entre fechas
            dates.append({
                'date_from': option[2].get('date_from'),
                'date_to':option[2].get('date_to')
            })
            date_to = datetime.strptime(option[2].get('date_to'), '%Y-%m-%d')
            for month in range(int(months_n)):
                new_date = date_to - relativedelta(months=month+1)
                new_date_from = '{}-{}-{}'.format(new_date.year,new_date.month, calendar.monthrange(new_date.year, new_date.month)[1])
                new_date_to = '{}-{}-01'.format(new_date.year,new_date.month)
                dates.append({
                    'date_from': new_date_from,
                    'date_to': new_date_to
                })
                date_names.append('Del {} Al {}'.format(new_date_to, new_date_from))
        else:
            dates.append({
                'date_from': option[2].get('date_from'),
                'date_to':option[2].get('date_to')
            })
        data = {
            'model': self,
            'company_id': option[1],
            'dates': dates,
        }
        data_report = self.get_report_data(data)
        return {
            'name': "Account Reports PandL",
            'type': 'ir.actions.client',
            'tag': 'account_extend_ikatech.values',
            'orders': data,
            'company_id': self.company_id,
            'data_report': data_report,
            'dates_name': date_names,
            'comparation': comparation,
        }

    def get_report_data(self, data):
        report_data = {
            'ingresos_brutos': [],
            'comision_clientes': [],
            'tot_net_incomes': [],
            'otros_ingresos': [],
            'total_ingresos': [],
            'costo_directo_op': [],
            'otros_costos_op': [],
            'margen_bruto_op': [],
            # Analitic lines
            'costo_directo_co':[],
            'comision_brokers': [],
            'margen_neto_op_vnt': [],
            'proveedores': [],
            'centro_atencion': [],
            'control_calidad': [],
            'ventas': [],
            'servicio_cliente': [],
            'costo_indirecto_op': [],
            'margen_neto': [],
            'operaciones': [],
            'comercial_mark': [],
            'gerencia': [],
            'legal_aud': [],
            'cont_fin': [],
            'admin_rh': [],
            'sistemas': [],
            'corpo': [],
            'meses_ant': [],
            'gst_gral': [],
            'ebitda': [],
            'costos_extraor': [],
            'ebitda_extra': [],
            'depre': [],
            'amort': [],
            'ebit': [],
            'ing_noop': [],
            'com_ban': [],
            'int_mul': [],
            'diversos': [],
            'no_dedu': [],
            'mult_san': [],
            'dif_cam': [],
            'imps': [],
            'gast_ejer_ant': [],
            'resul_neto': [],
            
        }
        
        for date in data['dates']:
            date_from = date['date_from']
            date_to = date['date_to']
            ib, cc, oi, cdo, ocp, cb = self.get_incomes_items(data['company_id'], date_from, date_to)
            cdc, pv, ca, ccal,vt,sc, op, cm, gr, la, cf, af, sis, cr, cext, dep, amort, msa = self.get_analytic_items(data['company_id'], date_from, date_to)
            ingoop, cob, inm, divs, ndd, mus, difc,imps, gea  = self.get_analytic_no_oper(data['company_id'], date_from, date_to)
            report_data['ingresos_brutos'].append(self.format_currency(ib))
            report_data['comision_clientes'].append(self.format_currency(cc))
            report_data['tot_net_incomes'].append(self.format_currency(ib - cc))
            report_data['otros_ingresos'].append(self.format_currency(oi))
            total_ingresos = (ib - cc) + oi
            report_data['total_ingresos'].append(self.format_currency(total_ingresos))
            report_data['costo_directo_op'].append(self.format_currency(cdo))
            report_data['otros_costos_op'].append(self.format_currency(ocp))
            margen_bruto_op = total_ingresos - cdo - ocp
            report_data['margen_bruto_op'].append(self.format_currency(margen_bruto_op))
            report_data['costo_directo_co'].append(self.format_currency(cdc))
            report_data['comision_brokers'].append(self.format_currency(cb))
            margen_neto_op_vnt = margen_bruto_op - cdc - cb
            report_data['margen_neto_op_vnt'].append(self.format_currency(margen_neto_op_vnt))
            report_data['proveedores'].append(self.format_currency(pv))
            report_data['centro_atencion'].append(self.format_currency(ca))
            report_data['control_calidad'].append(self.format_currency(ccal))
            report_data['ventas'].append(self.format_currency(vt))
            report_data['servicio_cliente'].append(self.format_currency(sc))
            costo_indirecto_op = pv + ca + ccal + vt + sc
            report_data['costo_indirecto_op'].append(self.format_currency(costo_indirecto_op))
            margen_neto = margen_neto_op_vnt - costo_indirecto_op
            report_data['margen_neto'].append(self.format_currency(margen_neto))
            report_data['operaciones'].append(self.format_currency(op))
            report_data['comercial_mark'].append(self.format_currency(cm))
            report_data['gerencia'].append(self.format_currency(gr))
            report_data['legal_aud'].append(self.format_currency(la))
            report_data['cont_fin'].append(self.format_currency(cf))
            report_data['admin_rh'].append(self.format_currency(af))
            report_data['sistemas'].append(self.format_currency(sis))
            report_data['corpo'].append(self.format_currency(cr))
            report_data['meses_ant'].append(self.format_currency(msa))
            gst_gral = op + cm + gr + la + cf + af + sis + cr + msa
            report_data['gst_gral'].append(self.format_currency(gst_gral))
            ebitda = margen_neto - gst_gral
            report_data['ebitda'].append(self.format_currency(ebitda))
            report_data['costos_extraor'].append(self.format_currency(cext))
            ebitda_extra = ebitda - cext
            report_data['ebitda_extra'].append(self.format_currency(ebitda_extra))
            report_data['depre'].append(self.format_currency(dep))
            report_data['amort'].append(self.format_currency(amort))
            ebit = ebitda_extra - (dep + amort)
            report_data['ebit'].append(self.format_currency(ebit))
            report_data['ing_noop'].append(self.format_currency(ingoop))
            report_data['com_ban'].append(self.format_currency(cob))
            report_data['int_mul'].append(self.format_currency(inm))
            report_data['diversos'].append(self.format_currency(divs))
            report_data['no_dedu'].append(self.format_currency(ndd))
            report_data['mult_san'].append(self.format_currency(mus))
            report_data['dif_cam'].append(self.format_currency(difc))
            report_data['imps'].append(self.format_currency(imps))
            report_data['gast_ejer_ant'].append(self.format_currency(gea))
            ing_no_ope = cob + inm + divs + ndd + mus + difc + imps + gea 
            resul_neto = (ebit + ingoop) - (ing_no_ope)
            report_data['resul_neto'].append(self.format_currency(resul_neto))
            
        return report_data
    
    def get_incomes_items(self, company_id, date_from, date_to):
        ingresos_brutos = sum(self.env['account.move.line'].search(
            self.get_domain('net_incomes', company_id, date_from, date_to)).mapped(lambda r: r.debit - r.credit))
        comision_clientes =  sum(self.env['account.move.line'].search(
            self.get_domain('customer_comissions', company_id, date_from, date_to)).mapped(lambda r: r.debit - r.credit))
        other_incomes = sum(self.env['account.move.line'].search(
            self.get_domain('other_incomes', company_id, date_from, date_to)).mapped(lambda r: r.debit - r.credit))
        direct_cost_op = sum(self.env['account.move.line'].search(
            self.get_domain('costo_directo_op', company_id, date_from, date_to)).mapped(lambda r: r.debit - r.credit))
        otros_costos_op = sum(self.env['account.move.line'].search(
            self.get_domain('otros_costos_op', company_id, date_from, date_to)).mapped(lambda r: r.debit - r.credit))
        comision_brokers = sum(self.env['account.move.line'].search(
            self.get_domain('comision_brokers', company_id, date_from, date_to)).mapped(lambda r: r.debit - r.credit))
        return abs(ingresos_brutos), abs(comision_clientes),  abs(other_incomes), abs(direct_cost_op), abs(otros_costos_op), abs(comision_brokers)
    
    def get_analytic_items(self, company_id, date_from, date_to):
        costo_directo_co = sum(self.env['account.analytic.line'].search(
            self.get_domain('costo_directo_co', company_id, date_from, date_to)).mapped('amount'))
        proveedores = sum(self.env['account.analytic.line'].search(
            self.get_domain('proveedores', company_id, date_from, date_to)).mapped('amount'))
        centro_atencion = sum(self.env['account.analytic.line'].search(
            self.get_domain('centro_atencion', company_id, date_from, date_to)).mapped('amount'))
        control_calidad = sum(self.env['account.analytic.line'].search(
            self.get_domain('control_calidad', company_id, date_from, date_to)).mapped('amount'))
        ventas = sum(self.env['account.analytic.line'].search(
            self.get_domain('ventas', company_id, date_from, date_to)).mapped('amount'))
        servicio_cliente = sum(self.env['account.analytic.line'].search(
            self.get_domain('servicio_cliente', company_id, date_from, date_to)).mapped('amount'))
        operaciones = sum(self.env['account.analytic.line'].search(
            self.get_domain('operaciones', company_id, date_from, date_to)).mapped('amount'))
        comercial_mark = sum(self.env['account.analytic.line'].search(
            self.get_domain('comercial_mark', company_id, date_from, date_to)).mapped('amount'))
        gerencia = sum(self.env['account.analytic.line'].search(
            self.get_domain('gerencia', company_id, date_from, date_to)).mapped('amount'))
        legal_aud = sum(self.env['account.analytic.line'].search(
            self.get_domain('legal_aud', company_id, date_from, date_to)).mapped('amount'))
        cont_fin = sum(self.env['account.analytic.line'].search(
            self.get_domain('cont_fin', company_id, date_from, date_to)).mapped('amount'))
        admin_rh = sum(self.env['account.analytic.line'].search(
            self.get_domain('admin_rh', company_id, date_from, date_to)).mapped('amount'))
        sistemas = sum(self.env['account.analytic.line'].search(
            self.get_domain('sistemas', company_id, date_from, date_to)).mapped('amount'))
        corpo = sum(self.env['account.analytic.line'].search(
            self.get_domain('corpo', company_id, date_from, date_to)).mapped('amount'))
        meses_ant = sum(self.env['account.analytic.line'].search(
            self.get_domain('meses_ant', company_id, date_from, date_to)).mapped('amount'))
        costos_extraor = sum(self.env['account.analytic.line'].search(
            self.get_domain('costos_extraor', company_id, date_from, date_to)).mapped('amount'))
        depre = sum(self.env['account.analytic.line'].search(
            self.get_domain('depre', company_id, date_from, date_to)).mapped('amount'))
        amort = sum(self.env['account.analytic.line'].search(
            self.get_domain('amort', company_id, date_from, date_to)).mapped('amount'))
        return abs(costo_directo_co), abs(proveedores), abs(centro_atencion), abs(control_calidad), abs(ventas), abs(servicio_cliente), abs(operaciones),abs(comercial_mark), abs(gerencia), abs(legal_aud), abs(cont_fin), abs(admin_rh), abs(sistemas), abs(corpo), abs(costos_extraor), abs(depre), abs(amort), abs(meses_ant)

    def get_analytic_no_oper(self, company_id, date_from, date_to):
        ing_noop = sum(self.env['account.analytic.line'].search(
            self.get_domain('ing_noop', company_id, date_from, date_to)).mapped('amount'))
        com_ban = sum(self.env['account.analytic.line'].search(
            self.get_domain('com_ban', company_id, date_from, date_to)).mapped('amount'))
        int_mul = sum(self.env['account.analytic.line'].search(
            self.get_domain('int_mul', company_id, date_from, date_to)).mapped('amount'))
        diversos = sum(self.env['account.analytic.line'].search(
            self.get_domain('diversos', company_id, date_from, date_to)).mapped('amount'))
        no_dedu = sum(self.env['account.analytic.line'].search(
            self.get_domain('no_dedu', company_id, date_from, date_to)).mapped('amount'))
        mult_san = sum(self.env['account.analytic.line'].search(
            self.get_domain('mult_san', company_id, date_from, date_to)).mapped('amount'))
        dif_cam = sum(self.env['account.analytic.line'].search(
            self.get_domain('dif_cam', company_id, date_from, date_to)).mapped('amount'))
        imps = sum(self.env['account.analytic.line'].search(
            self.get_domain('imps', company_id, date_from, date_to)).mapped('amount'))
        gast_ejer_ant = sum(self.env['account.analytic.line'].search(
            self.get_domain('gast_ejer_ant', company_id, date_from, date_to)).mapped('amount'))
        return abs(ing_noop), abs(com_ban), abs(int_mul), abs(diversos), abs(no_dedu), abs(mult_san), abs(dif_cam), abs(imps),  abs(gast_ejer_ant), 
    
    @api.model
    def show_detail_data(self, account_id, date_from, date_to):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Detalle de Cuenta',
            'res_model': 'account.move.line',
            'view_type': 'list',
            'view_mode': 'list',
            'target': 'current',
            'views': [[self.env.ref('account.view_move_line_tree').id, 'list']],
            'domain': [('account_id.id','=', account_id),('date', '>=', date_to), ('date','<=',date_from), ('parent_state','=','posted')],
            'context': "{'create': False}",
        }
    
    @api.model
    def show_detail_data_analytic(self, account_id, company_id, date_from, date_to, type_operation):
        domain = self.get_domain_show_detail(type_operation, company_id, date_from, date_to, account_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Detalle de Apuntes Analiticos',
            'res_model': 'account.analytic.line',
            'view_type': 'list',
            'view_mode': 'list',
            'target': 'current',
            'views': [[self.env.ref('analytic.view_account_analytic_line_tree').id, 'list']],
            'domain': domain,
            'context': "{'create': False}",
        }
    
    @api.model
    def get_details_lines(self, option, company_id, type_operation, row_id, date_from, date_to, comparation, months):
        dates = []
        if comparation: # Si hay que comparar entre fechas
            dates.append({
                'date_from': date_from,
                'date_to':date_to
            })
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            for month in range(int(months)):
                new_date = date_to - relativedelta(months=month+1)
                new_date_from = '{}-{}-{}'.format(new_date.year,new_date.month, calendar.monthrange(new_date.year, new_date.month)[1])
                new_date_to = '{}-{}-01'.format(new_date.year,new_date.month)
                dates.append({
                    'date_from': new_date_from,
                    'date_to': new_date_to
                })
        else:
            dates.append({
                'date_from': date_from,
                'date_to':date_to
            })
        data_comparation = []
        i = 1
        no_data = False
        for date in dates:
            if comparation == False:
                domain = self.get_domain(type_operation, company_id, date['date_from'], date['date_to'])
                data = self.get_data_move_line(domain, type_operation)
            else:
                domain = self.get_domain(type_operation, company_id, date['date_from'], date['date_to'])
                data = self.get_data_move_line(domain, type_operation)
                if not data_comparation:
                    i = i + 1
                    if no_data:
                        for line in data:
                            line['amount'].insert(0,self.format_currency(0))
                    if not data:
                        no_data = True
                    data_comparation = data
                    continue
                for line in data:
                    find = False
                    for dc in data_comparation:
                        if dc['id'] == line['id']:
                            dc['amount'].append(line['amount'][0])
                            find = True
                    if not find:
                        amounts = []
                        for x in range(i - 1):
                            amounts.append(self.format_currency(0))
                        amounts.append(line['amount'][0])
                        data_comparation.append({
                            'id': line['id'],
                            'name': line['name'],
                            'amount': amounts,
                        })
                for dc in data_comparation:
                    if len(dc['amount']) <= i:
                        for x in range(i - len(dc['amount'])):
                            dc['amount'].append(self.format_currency(0))
                i = i + 1
        new_data = data if comparation == False else data_comparation
        return {
            'name': "Account Reports PandL",
            'type': 'ir.actions.client',
            'tag': 'account_extend_ikatech.detail_incomes',
            'data': new_data,
            'type_operation': type_operation,
            'idRow': row_id,
            'dates': dates,
        }

            
    #! --------------------------------------------      
    @api.model
    def get_analytics_account(self, option, company_id, account_id, date_from, date_to, comparation, months):
        dates = []
        if comparation: # Si hay que comparar entre fechas
            dates.append({
                'date_from': date_from,
                'date_to':date_to
            })
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
            for month in range(int(months)):
                new_date = date_to - relativedelta(months=month+1)
                new_date_from = '{}-{}-{}'.format(new_date.year,new_date.month, calendar.monthrange(new_date.year, new_date.month)[1])
                new_date_to = '{}-{}-01'.format(new_date.year,new_date.month)
                dates.append({
                    'date_from': new_date_from,
                    'date_to': new_date_to
                })
        else:
            dates.append({
                'date_from': date_from,
                'date_to':date_to
            })
        data_comparation = []
        i = 1
        no_data = False
        for date in dates:
            if comparation == False:
                lines = self.env['account.move.line'].read_group(
                        [
                            ('account_id.id','=', account_id),
                            ('company_id', '=', company_id),('parent_state','=','posted'),
                            ('date', '>=', date['date_to']), ('date','<=',date['date_from']),
                        ],
                        ['analytic_account_id','debit:sum','credit:sum'],
                        ['analytic_account_id']
                    )
                data = []
                for line in lines:
                    analytic_account = line.get('analytic_account_id')[1]
                    amount = line.get('debit') - line.get('credit')
                    if amount != 0:
                        data.append({
                            'id': line.get('analytic_account_id')[0],
                            'name': analytic_account,
                            'amount': [self.format_currency(amount)],
                        })
            else:
                data = []
                # primero consulta la primer fecha
                lines = self.env['account.move.line'].read_group(
                        [
                            ('account_id.id','=', account_id),
                            ('company_id', '=', company_id),('parent_state','=','posted'),
                            ('date', '>=', date['date_to']), ('date','<=',date['date_from']),
                        ],
                        ['analytic_account_id','debit:sum','credit:sum'],
                        ['analytic_account_id']
                    )
                for line in lines: # llenamos el arreglo que vamos a usar para las operaciones
                    analytic_account = line.get('analytic_account_id')[1]
                    amount = line.get('debit') - line.get('credit')
                    if amount != 0:
                        data.append({
                            'id': line.get('analytic_account_id')[0],
                            'name': analytic_account,
                            'amount': [self.format_currency(amount)],
                        })
                if not data_comparation: #los datos de la primer fecha siempre se van a pasar a un nuevo arreglo
                    data_comparation = data
                    if not data: # si no existe ninguna concidencia en la primer fecha, tenemos que identificar que no existe data
                        no_data = True
                    if no_data: # si no se encontro data en la fecha anterior, vamos a agregar un cero al inicio del arreglo de la cantidad para simular la fecha anterior calculada ya que no obtuvimos datos
                        for line in data:
                            line['amount'].insert(0,self.format_currency(0))
                    i = i + 1 # y aqui se va aumentar la posición del arreglo de las cantidades ya que la primer fecha se establecio y se va a brincar a la segunda
                    continue
                for line in data: # la primera fecha fue calculada. ahora proseguimos a colocar los datos de la segunda fecha en el arreglo de la primera
                    find = False
                    for dc in data_comparation:
                        if dc['id'] == line['id']:
                            dc['amount'].append(line['amount'])
                            find = True
                    if not find:
                        amounts = []
                        for x in range(i - 1): #si en esta fecha la cuenta contable no tuvo resultados con la anterior fecha, proseguimos a insertarla en el arreglo con la cantidad de ceros correspondinete a las fechas previameinta calculadas
                            amounts.append(self.format_currency(0))
                        amounts.append(line['amount'])
                        data_comparation.append({
                            'id': line['id'],
                            'name': line['name'],
                            'amount': amounts,
                        })
                for dc in data_comparation: #si alguna cuenta de la fecha anterior no tuvo concidencia con la siguiente, agregar en ceros las cuentas que no tuvieron concidencias
                    if len(dc['amount']) <= i:
                        for x in range(i - len(dc['amount'])):
                            dc['amount'].append(self.format_currency(0))
                i = i + 1
        new_data = data if comparation == False else data_comparation
        # ? . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
        return {
            'name': "Account Reports PandL",
            'type': 'ir.actions.client',
            'tag': 'account_extend_ikatech.detail_incomes',
            'data': new_data,
            'idAccount': account_id,
            'dates': dates,
        }

    @api.model
    def show_amount_analytic_detail(self, account_id, date_from, date_to, analytic_id):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Detalle de Cuenta',
            'res_model': 'account.move.line',
            'view_type': 'list',
            'view_mode': 'list',
            'target': 'current',
            'views': [[self.env.ref('account.view_move_line_tree').id, 'list']],
            'domain': [('account_id.id','=', account_id),('analytic_account_id.id','=', analytic_id),('date', '>=', date_to), ('date','<=',date_from), ('parent_state','=','posted')],
            'context': "{'create': False}",
        }

    #! Tools 
    def format_currency(self, amount):
        return "$ {:,.2f}".format(amount)
    
    def get_data_move_line(self, domain, type_operation):
        aml = ('net_incomes','customer_comissions','other_incomes','costo_directo_op','otros_costos_op','comision_brokers')
        data = []
        if type_operation in aml:
            lines = self.env['account.move.line'].read_group(
                domain,
                ['account_id','debit:sum','credit:sum'],
                ['account_id']
            )  
            for line in lines:
                account = line.get('account_id')[1]
                amount = line.get('debit') - line.get('credit')
                if amount != 0:
                    data.append({
                        'id': line.get('account_id')[0],
                        'name': account,
                        'amount': [self.format_currency(amount)],
                    })
        else:
            lines = self.env['account.analytic.line'].read_group(
                    domain,
                    ['general_account_id','amount:sum'],
                    ['general_account_id']
                )  
            for line in lines:
                account = line.get('general_account_id')[1]
                amount = line.get('amount')
                if amount != 0:
                    data.append({
                        'id': line.get('general_account_id')[0],
                        'name': account,
                        'amount': [self.format_currency(amount)],
                    })
        return data
    
    def get_domain(self, type_operation, company_id, date_from, date_to):
        domain = False
        if type_operation == 'net_incomes':
            domain = [
                ('account_id.user_type_id','=',13), #Incomes
                ('account_id.code','not in',('40008001','40008002','40008003')),
                ('company_id', '=', company_id), ('parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'customer_comissions':
            domain = [
                ('account_id.code','=','52010001'),
                ('company_id', '=', company_id),
                ('parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'other_incomes':
            domain = [
                ('account_id.code','in',('40008001','40008002','40008003')),
                ('company_id', '=', company_id),('parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'costo_directo_op':
            domain = [
                ('account_id.user_type_id','=',17), #costo de ingreso
                ('account_id.code','not in',('52010001','50008001','53000003','59000001')),
                ('company_id', '=', company_id),('parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'otros_costos_op':
            domain = [
                ('account_id.code','in',('50008001','53000003','59000001')),
                ('company_id', '=', company_id),('parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]    
        if type_operation == 'costo_directo_co':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=',78), # Comercialización
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'comision_brokers':
            domain = [
                ('account_id','=','52025001'), # Comercialización
                ('company_id', '=', company_id), ('parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'proveedores':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=',63), # Proveedores
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'centro_atencion':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=',62), # Centro Atencion Telefonica
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'control_calidad':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=',64), # Control Calidad
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'ventas':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=',2653), # Ventas
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'servicio_cliente':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 66), # Servicio Cliente
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'operaciones':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 61), # operaciones
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'comercial_mark':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 65), # COMERCIAL/MARKETING
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'gerencia':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 67), # Gerencia
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'legal_aud':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 68), # LEGAL / AUDITORÍA
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'cont_fin':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 69), # CONTABILIDAD Y FINANZAS
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'admin_rh':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 70), # ADM Y RRHH
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'sistemas':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 71), # sistemas
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'corpo':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 72), # Corporativo
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'meses_ant':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 7635), # Gastos meses anteriores
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'costos_extraor':
            domain = [
                ('general_account_id.user_type_id','in',(15,20)), #gastos y otros gastos
                ('account_id','=', 76), # Extraordinarios
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'depre':
            domain = [
                ('general_account_id.user_type_id','=',16), #depreciacion
                ('general_account_id.code','not ilike', '6505%'), 
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'amort':
            domain = [
                ('general_account_id.code','ilike', '6505'),
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'ing_noop':
            domain = [
                ('general_account_id.user_type_id','=',14), #otros ingresos
                ('account_id','=', 75), # No operaciones
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'com_ban':
            domain = [
                ('general_account_id.code','in', ('72001002','72001004','72001001','72005002')),
                ('account_id','=', 75), # No operacionales
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'int_mul':
            domain = [
                ('general_account_id.code','=','72001003'),
                ('account_id','=', 75), # No operacionales
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'diversos':
            domain = [
                ('general_account_id.user_type_id','=', 15), #gastos
                ('general_account_id.code','in', ('72005002','72008001')),
                ('general_account_id.code','not ilike', ('65%')),
                ('account_id','in', (75, 74, 86)), # No operacionales, vps, presidencia
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'no_dedu':
            domain = [
                ('general_account_id.code','in',('61010098','62066018','62066019')),
                ('account_id','=', 75), # No operacionales
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'mult_san':
            domain = [
                ('general_account_id.code','=','620660219'),
                ('account_id','=', 75), # No operacionales
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'dif_cam':
            domain = [
                ('general_account_id.code','in',(
                    '70003001','70003002',
                    '70003003','70004001',
                    '72003001','72005003',
                    '72005004','72005005'
                )),
                ('account_id','=', 75), # No operacionales
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'imps':
            domain = [
                ('general_account_id.code','in',(
                    '60011001','62035004',
                    '62066001','62066002',
                    '62066005','62066006',
                    '62066007','62066011',
                    '62066022','62066027',
                    '62066028','62066029',
                    '72002001','72004001',
                    '72004002','72005001'
                )),
                ('account_id','=', 75), # No operacionales
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'gast_ejer_ant':
            domain = [
                ('general_account_id.code','=','62066020'),
                ('account_id','=', 75), # No operacionales
                ('company_id', '=', company_id), ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        return domain
    
    def get_domain_show_detail(self, type_operation, company_id, date_from, date_to, general_account_id):
        domain = False
        if type_operation == 'costo_directo_co':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=',78), # Comercialización
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'proveedores':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=',63), # Proveedores
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'centro_atencion':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=',62), # Centro Atencion Telefonica
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'control_calidad':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=',64), # Control Calidad
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'ventas':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=',2653), # Ventas
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'servicio_cliente':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 66), # Servicio Cliente
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'operaciones':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 61), # operaciones
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'comercial_mark':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 65), # COMERCIAL/MARKETING
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'gerencia':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 67), # Gerencia
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'legal_aud':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 68), # LEGAL / AUDITORÍA
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'cont_fin':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 69), # CONTABILIDAD Y FINANZAS
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'admin_rh':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 70), # ADM Y RRHH
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'sistemas':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 71), # sistemas
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'corpo':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 72), # Corporativo
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'meses_ant':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 7635), # meses anteriores
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'costos_extraor':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 76), # Extraordinarios
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'depre':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'amort':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'ing_noop':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operaciones
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'com_ban':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operacionales
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'int_mul':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operacionales
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'diversos':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','in', (75, 74, 86)), # No operacionales, vps, presidencia
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'no_dedu':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operacionales
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'mult_san':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operacionales
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'dif_cam':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operacionales
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'imps':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operacionales
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        if type_operation == 'gast_ejer_ant':
            domain = [
                ('general_account_id.id','=', general_account_id),
                ('account_id.id','=', 75), # No operacionales
                ('move_id.parent_state','=','posted'),
                ('date', '>=', date_to), ('date','<=',date_from),
            ]
        return domain