from odoo import models
import textwrap


class XmlPolizasExportWizard(models.TransientModel):
    _inherit = 'l10n_mx_xml_polizas.xml_polizas_wizard'

    def _get_move_export_data(self, accounts_results):
        # Retrieve extra data for CompNal node

        mx_move_vals = {}
        AccountMove = self.env['account.move']
        for results in accounts_results:
            lines_data = results[1][0].get('lines', [])
            for line_data in lines_data:
                # move line data is already grouped by account, we store the retrieved move info
                # to reduce db queries
                move_id = line_data['move_id']
                #for testing ivan_porras
                #move_id = 1023983
                mx_data = mx_move_vals.get(move_id)
                if not mx_data:
                    # uuid = AccountMove.browse(move_id).l10n_mx_edi_cfdi_uuid
                    #uuid = AccountMove.browse(move_id).l10n_mx_xml_poliza_uuid
                    partner_rfc = False
                    if line_data['country_code'] != 'MX':
                        partner_rfc = 'XEXX010101000'
                    elif line_data['partner_vat']:
                        partner_rfc = line_data['partner_vat'].strip()
                    elif line_data['country_code'] in (False, 'MX'):
                        partner_rfc = 'XAXX010101000'
                    else:
                        partner_rfc = 'XEXX010101000'

                    mx_data = {
                        'partner_rfc': partner_rfc,
                        #'l10n_mx_edi_cfdi_uuid': uuid,
                        'l10n_mx_edi_cfdi_uuid': False,
                    }
                    mx_move_vals[move_id] = mx_data
                #if mx_data.get('l10n_mx_edi_cfdi_uuid'):
                if mx_data.get('partner_rfc'):
                    currency_name = line_data.pop('currency_name', False)
                    currency_conversion_rate = mx_data.get('currency_conversion_rate')
                    foreign_currency = line_data['currency_id'] and line_data['currency_id'] != line_data[
                        'company_currency_id']
                    amount_total = line_data['amount_currency'] if foreign_currency else line_data['balance']
                    if foreign_currency and not currency_conversion_rate:
                        # calculate conversion rate just once per move so we don't see
                        # rounding differences between lines
                        amount_total_signed = line_data['balance']
                        if amount_total:
                            currency_conversion_rate = abs(amount_total_signed) / abs(amount_total)
                        else:
                            currency_conversion_rate = 1
                        currency_conversion_rate = '%.*f' % (5, currency_conversion_rate)
                        mx_data['currency_name'] = currency_name
                        mx_data['currency_conversion_rate'] = currency_conversion_rate
                    line_data.update({
                        'amount_total': amount_total,
                        **mx_data
                    })
        return super()._get_move_export_data(accounts_results)


    def _get_move_line_export_data(self, line):
        uuids = self.env['account.move.line'].search([('id','=',int(line['id']))]).eaccount_complements_ids
        lst_uuids = []
        for u in uuids:
            lst_uuids.append({'uuid':u.uuid,'amount':u.amount})
        currency = self.env['res.currency'].search([('id','=',int(line['currency_id']))])
        return {
            'line_label': textwrap.shorten(
                line['journal_name'] + ((' - ' + line['name']) if line['name'] else ''),
                width=200),
            'account_name': line['account_name'],
            'account_code': line['account_code'],
            'credit': '%.2f' % line['credit'],
            'debit': '%.2f' % line['debit'],
            'lst_uuid': lst_uuids,
            'currency_name': currency.name,
            'customer_vat': line['partner_rfc'],
            'currency_conversion_rate': line['currency_conversion_rate'] if 'currency_conversion_rate' in line else 1,
            #'amount_total': '%.2f' % line['amount_total'],
        }