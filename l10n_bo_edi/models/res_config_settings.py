import logging
import asyncio
from odoo.exceptions import UserError, Warning, ValidationError


from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    # l10n_bo_dfe_service_provider = fields.Selection(related='company_id.l10n_bo_dfe_service_provider', readonly=False,
    #                                                 help='Please select your company service provider for DFE service.')
    # # l10n_cl_activity_description = fields.Char(
    # #     string='Glosa Giro', related='company_id.l10n_cl_activity_description', readonly=False)
    # l10n_bo_company_activity_ids = fields.Many2many('l10n_bo.company.activities', string='Activities Names',
    #                                                 related='company_id.l10n_bo_company_activity_ids', readonly=False,
    #                                                 help='Please select the SIN registered economic activities codes for the company')

    l10n_bo_sync_time = fields.Datetime(
        string='Sync Time', help='Set the synchronization time for the SIN values')

    # SIN Codes

    l10n_bo_system_code = fields.Text(
        string='System Code', help='Code given by SIN in order to emit invoices')

    l10n_bo_CUIS_code = fields.Text(
        string='CUIS Code', help='Code given by SIN in order to emit electronic invoices')

    # l10n_bo_current_cuf = fields.Text(
    #     string='Current CUF Code', help='(Código Unico de Facturación) Code referred to Point of Attention', readonly=True)

    l10n_bo_current_cufd = fields.Text(
        string='Current CUFD Code', help='(Código Unico de Facturación Diaria) Code provided by SIN, generated daily, identifies the invoice along with a number', readonly=True)

    ###

    # Selling Points

    l10n_bo_active_selling_point = fields.Many2one(
        comodel_name='selling_point', string='Active Attention Point')

    l10n_bo_current_invoice_number = fields.Text(
        string='Current Invoice Number', help='Along with CUFD Code, helps in identifying the invoice', readonly=True)

    ###

    l10n_bo_invoicing_modality = fields.Many2one(
        'modalities', string='Modality Selection')

    l10n_bo_emission_type = fields.Many2one(
        'emission_types', string='Emission Type Selection')

    l10n_bo_sector_type = fields.Many2one(
        'sector_types', string='Sector Type Selection')

    l10n_bo_ambience = fields.Many2one('ambience', string='Ambience')

    l10n_bo_invoice_package_number = fields.Integer(
        string='Package Number', help='Set the number of invoices per package')

    module_l10n_bo_reports = fields.Boolean(string='Accounting Reports')

    l10n_bo_invoicing_type = fields.Boolean('Invoicing Type')

    l10n_bo_graphic_rep_format = fields.Boolean('Graphic Representation Format')

    l10n_bo_graphic_rep_size = fields.Boolean('Graphic Representation Size')

    ##TODO Agregar param readonly para modo Online Offline:
    l10n_bo_invoicing_current_status = fields.Boolean('Current Status (Offline/Online)', default = True)

    invoice_incident = fields.Selection(string='Invoice Event Demo', selection=[('inter1', 'CORTE DE SERVICIO DE INTERNET'),
                                                                                ('ws', 'INACCESIBILIDAD AL SERVICIO WEB DE LA ADMINISTRACIÓN TRIBUTARIA'),
                                                                                ('inter2', 'INGRESO A ZONAS SIN INTERNET POR DESPLIEGUE DE PUNTO DE VENTA EN VEHICULOS AUTOMOTORES'),
                                                                                ('inter3', 'VENTA EN LUGARES SIN INTERNET')])
    

    prov_dosage_edit = fields.Boolean('Provisional dosage data', default = False)

    external_con = fields.Boolean(string='External Connection', default = False) ##TODO no guarda en render
    

    # @api.onchange('l10n_bo_invoicing_type')
    # def _invoice_type_change(self):
    #     if self.l10n_bo_invoicing_type == False:
    #         for i in self.env['account.move'].search([]):
    #             i.e_billing = False
    #     else:
    #         for i in self.env['account.move'].search([]):
    #             i.e_billing = True

    # @api.onchange('l10n_bo_graphic_rep_format')
    # def _graphic_format_change(self):
    #     if self.l10n_bo_graphic_rep_format == False:
    #         for i in self.env['account.move'].search([]):
    #             i.representation_format = False
    #     else:
    #         for i in self.env['account.move'].search([]):
    #             i.representation_format = True
    
    # @api.onchange('l10n_bo_graphic_rep_size')
    # def _graphic_size_change(self):
    #     if self.l10n_bo_graphic_rep_size == False:
    #         for i in self.env['account.move'].search([]):
    #             i.representation_size = False
    #     else:
    #         for i in self.env['account.move'].search([]):
    #             i.representation_size = True

    # @api.onchange('l10n_bo_invoicing_current_status') ## No usar onchange. gatilla cada vez qie se realiza una accion en settings
    def _cert_status_change(self):
        ## Vars
        cert_status = self.env['bo_edi_params'].search( ## Variable de certificacion para cambio de estado Online/Offline
            [('name', '=', 'CERTSTATUS')])
        emission_type_obj = self.env['bo_edi_params'].search(
            [('name', '=', 'TIPOEMISION')])
        status_obj = self.env['bo_edi_params'].search(
            [('name', '=', 'ONLINE')])

        if self.l10n_bo_invoicing_current_status:
            asyncio.run(self.env['account.move'].send_package_settings())
            status_obj.write({"value" : 1})
            emission_type_obj.write({"value" : 1})
            cert_status.write({"value" : 1})
        else:
            cert_status.write({"value" : 0})

    @api.onchange('invoice_incident')
    def _inv_incident_change(self):
        demo_internet_status = self.env['bo_edi_params'].search(
            [('name', '=', 'DEMO_INT_STATUS')])
        demo_ws_status = self.env['bo_edi_params'].search(
            [('name', '=', 'DEMO_WS_STATUS')])
        if self.invoice_incident == 'ws':
            demo_internet_status.write({"value" : 1})
            demo_ws_status.write({"value" : 0})
        else:
            demo_internet_status.write({"value" : 0})
            demo_ws_status.write({"value" : 1})

    def generate_cufd(self):
        if self.env['account.move'].getBranchOffice()[1] and self.env['account.move'].getBranchOffice()[2]:
            new_cufd = asyncio.run(self.env['account.move'].create_new_CUFD())
            print(new_cufd[0])
        else:
            raise Warning('The current user doesn''t have branch office nor a selling point configured')
        # aux_date = self.getTime()
        # sec_date = datetime(aux_date.year, aux_date.month, aux_date.day).strftime("%Y-%m-%d")
        # prueba = self.env['sin_token'].search(['&', (
        #             'begin_date',
        #             '<=', sec_date),
        #             ('end_date',
        #             '>=', sec_date)])
        # print(aux_date)
        # print(sec_date)
        # print(prueba.begin_date)
        # print(prueba.end_date)

    # Metodos Requeridos para el correcto registro y obtencion

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.l10n_bo_invoicing_type', self.l10n_bo_invoicing_type)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.l10n_bo_graphic_rep_format', self.l10n_bo_graphic_rep_format)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.l10n_bo_graphic_rep_size', self.l10n_bo_graphic_rep_size)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.l10n_bo_invoicing_current_status', self.l10n_bo_invoicing_current_status)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.prov_dosage_edit', self.prov_dosage_edit)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.invoice_incident', self.invoice_incident)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.external_con', self.external_con)

        self._cert_status_change()
        # self.env['ir.config_parameter'].sudo().set_param(
        #     'res.config.settings.l10n_bo_emission_type', self.l10n_bo_emission_type)
        # self.env['ir.config_parameter'].sudo().set_param(
        #     'res.config.settings.l10n_bo_invoicing_modality', self.l10n_bo_invoicing_modality)
        # self.env['ir.config_parameter'].sudo().set_param(
        #     'res.config.settings.l10n_bo_ambience', self.l10n_bo_ambience)
        # self.env['ir.config_parameter'].sudo().set_param(
        #     'res.config.settings.l10n_bo_system_code', self.l10n_bo_system_code)
        # self.env['ir.config_parameter'].sudo().set_param(
        #     'res.config.settings.l10n_bo_CUIS_code', self.l10n_bo_CUIS_code)
        # self.env['ir.config_parameter'].sudo().set_param(
        #     'res.config.settings.l10n_bo_invoice_package_number', self.l10n_bo_invoice_package_number)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        get_invoicing_type = get_param(
            'res.config.settings.l10n_bo_invoicing_type')
        get_graphic_rep_format = get_param(
            'res.config.settings.l10n_bo_graphic_rep_format')
        get_graphic_rep_size = get_param(
            'res.config.settings.l10n_bo_graphic_rep_size')
        get_current_status = get_param(
            'res.config.settings.l10n_bo_invoicing_current_status')
        get_prov_dosage_edit = get_param(
            'res.config.settings.prov_dosage_edit')
        get_invoice_incident = get_param(
            'res.config.settings.invoice_incident')
        get_external_con = get_param(
            'res.config.settings.external_con')
        # get_invoicing_modality = get_param(
        #     'res.config.settings.l10n_bo_invoicing_modality')
        # get_ambience = get_param(
        #     'res.config.settings.l10n_bo_ambience')
        res.update(
            l10n_bo_invoicing_type = get_invoicing_type,
            l10n_bo_graphic_rep_format = get_graphic_rep_format,
            l10n_bo_graphic_rep_size = get_graphic_rep_size,
            l10n_bo_invoicing_current_status = get_current_status,
            prov_dosage_edit = get_prov_dosage_edit,
            invoice_incident = get_invoice_incident,
            external_con = get_external_con
            # l10n_bo_invoicing_modality=get_invoicing_modality,
            # l10n_bo_ambience=get_ambience
        )
        return res
