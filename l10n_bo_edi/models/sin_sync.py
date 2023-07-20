from asyncio import streams
from odoo import fields, models
from pytz import timezone
from datetime import datetime, timedelta

import zeep
from zeep import client
import logging

import codecs
import socket

_logger = logging.getLogger(__name__)


class SinSync(models.Model):
    _name = 'sin_sync'
    _description = 'Recurrent SIN Api calls'

    def _getDate(self):
        now = datetime.now(
            timezone('America/La_Paz')).strftime("%Y-%m-%d")
        return now

    def get_token(self):
        # return self.env['bo_edi_params'].search(
        #     [('name', '=', 'TOKENAPI')]).value
        today = self._getDate()
        token_obj = self.env['sin_token'].search(['&', (
                    'begin_date',
                    '<=', today),
                    ('end_date',
                    '>=', today)])
        if token_obj:
            return token_obj
        else:
            return False

    def _get_url_sync_datos(self):
        return self.env['bo_edi_params'].search(
            [('name', '=', 'URL_SYNC_DATOS')]).value
    
    def _get_url_recep_comp(self):
        return self.env['bo_edi_params'].search(
            [('name', '=', 'URL_RECEP_COMP')]).value

    def _get_url_op(self):
        return self.env['bo_edi_params'].search(
            [('name', '=', 'URL_OP')]).value

    def _get_url_obt_cod(self):
        return self.env['bo_edi_params'].search(
            [('name', '=', 'URL_OBT_COD')]).value
    
    def _get_url_comp_vent(self):
        return self.env['bo_edi_params'].search(
            [('name', '=', 'URL_COMP_VENT')]).value

    # SERVICIO DE OBTENCIÓN DE CÓDIGOS

    def check_communication(self):
        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_obt_cod(),
            settings=settings)
        result = client.service.verificarComunicacion()
        return result.mensajesList[0]

    async def get_cufd(self, ambiente, modalidad, puntoventa, codSistema, codSucursal, cuis, nit, tipoCodigo):
        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_obt_cod(),
            settings=settings)
        params = {'SolicitudCufd': {
            'codigoAmbiente': ambiente,
            'codigoModalidad': modalidad,
            'codigoPuntoVenta': puntoventa,
            'codigoSistema': codSistema,
            'codigoSucursal': codSucursal,
            'cuis': cuis,
            'nit': nit
        }
        }
        result = client.service.cufd(**params)
        if (tipoCodigo == 0):  # CodigoControl
            return result.codigoControl
        elif(tipoCodigo == 1):  # CUFD
            return result.codigo
        else: 
            return result

    # SERVICIO DE SINCRONIZACIÓN DE DATOS

    def sync_general(self, ambiente, puntoventa, codSistema, codSucursal, cuis, nit):
        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_sync_datos(),
            settings=settings)
        params = {'SolicitudSincronizacion': {
            'codigoAmbiente': ambiente,
            'codigoPuntoVenta': puntoventa,
            'codigoSistema': codSistema,
            'codigoSucursal': codSucursal,
            'cuis': cuis,
            'nit': nit
        }
        }
        return {'client': client, 'params': params, 'ambience': ambiente}

    def sync_activities(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarActividades(**params)

        if (ambiente == 1):
            activities = self.env['l10n_bo.company.activities']
            activities.search([]).unlink()
            print(activities.search([]))
            for activity in result.listaActividades:
                new_record = {
                    'code': activity.codigoCaeb,
                    'name': activity.descripcion,
                    'type': activity.tipoActividad
                }
                activities.create(new_record)
            for act in activities.search([]).name:
                print(act.type)

        # Método para comparacion de registros existentes y adicion de nuevos pendiente
        # for activity in result.listaActividades:
        #     db_activity = self.env['l10n_bo.company.activities'].search(
        #         [('code', '=', activity.codigoCaeb)])
        #     print(db_activity.name)
        #     if not hasattr(db_activity, 'code'):
        #         new_record = {
        #             'code': activity.codigoCaeb,
        #             'name': activity.descripcion,
        #             'type': activity.tipoActividad
        #         }
        #         self.env['l10n_bo.company.activities'].create(new_record)
        #         print('Nuevos registros: ')
        #         print(self.env['l10n_bo.company.activities'].search([]))

    def sync_fecha_hora(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarFechaHora(**params)
        
        return result
        # date_time = self.env['boedi_date_time']
        # if (ambiente == 1):
        #     date_time.search([]).unlink()
        #     new_record = {
        #         'date_time': result.fechaHora
        #     }
        #     date_time.create(new_record)

        # print(date_time.search([]).date_time)

    def sync_actividades_doc_sector(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarListaActividadesDocumentoSector(
            **params)

        if (ambiente == 1):
            activities_doc_sec = self.env['activity_doc_sector']
            activities_doc_sec.search([]).unlink()
            print(activities_doc_sec.search([]))
            for act_doc_sec in result.listaActividadesDocumentoSector:
                new_record = {
                    'activity_code': act_doc_sec.codigoActividad,
                    'sector_doc_code': act_doc_sec.codigoDocumentoSector,
                    'sector_doc_type': act_doc_sec.tipoDocumentoSector
                }
                activities_doc_sec.create(new_record)
            for act in activities_doc_sec.search([]):
                print(act.activity_code)

    def sync_invoice_caption(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarListaLeyendasFactura(
            **params)

        if (ambiente == 1):
            inv_caption = self.env['invoice_caption']
            inv_caption.search([]).unlink()
            print(inv_caption.search([]))
            for inv_cap in result.listaLeyendas:
                new_record = {
                    'activity_code': inv_cap.codigoActividad,
                    'description': inv_cap.descripcionLeyenda
                }
                inv_caption.create(new_record)
            for cap in inv_caption.search([]):
                print(cap.description)

    def sync_messages_service(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarListaMensajesServicios(
            **params)

        if (ambiente == 1):
            message_serv = self.env['messages_service']
            message_serv.search([]).unlink()
            print(message_serv.search([]))
            for mes_serv in result.listaCodigos:
                new_record = {
                    'code': mes_serv.codigoClasificador,
                    'description': mes_serv.descripcion
                }
                message_serv.create(new_record)
            for mes in message_serv.search([]):
                print(mes.description)

    def sync_sin_items(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarListaProductosServicios(
            **params)

        if (ambiente == 1):
            sin_items = self.env['sin_items']
            sin_items.search([]).unlink()
            print(sin_items.search([]))
            for sin_item in result.listaCodigos:
                new_record = {
                    'sin_code': sin_item.codigoProducto,
                    'description': sin_item.descripcionProducto,
                    'activity_code': sin_item.codigoActividad
                }
                sin_items.create(new_record)
            for item in sin_items.search([]):
                print(item.description)

    def sync_invoice_events(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaEventosSignificativos(
            **params)

        if (ambiente == 1):
            invoice_event = self.env['invoice_event']
            invoice_event.search([]).unlink()
            print(invoice_event.search([]))
            for inv_ev in result.listaCodigos:
                new_record = {
                    'code': inv_ev.codigoClasificador,
                    'description': inv_ev.descripcion
                }
                invoice_event.create(new_record)
            for inv in invoice_event.search([]):
                print(inv.description)

    def sync_null_reasons(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaMotivoAnulacion(
            **params)

        if (ambiente == 1):
            null_reason = self.env['null_reason']
            null_reason.search([]).unlink()
            print(null_reason.search([]))
            for null_re in result.listaCodigos:
                new_record = {
                    'code': null_re.codigoClasificador,
                    'description': null_re.descripcion
                }
                null_reason.create(new_record)
            for reas in null_reason.search([]):
                print(reas.description)

    def sync_native_country(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaPaisOrigen(
            **params)

        if (ambiente == 1):
            native_country = self.env['native_country']
            native_country.search([]).unlink()
            print(native_country.search([]))
            for nat_co in result.listaCodigos:
                new_record = {
                    'code': nat_co.codigoClasificador,
                    'description': nat_co.descripcion
                }
                native_country.create(new_record)
            for nat in native_country.search([]):
                print(nat.description)

    def sync_id_type(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTipoDocumentoIdentidad(
            **params)

        if (ambiente == 1):
            id_type = self.env['id_type']
            id_type.search([]).unlink()
            print(id_type.search([]))
            for id_t in result.listaCodigos:
                new_record = {
                    'id_type_code': id_t.codigoClasificador,
                    'description': id_t.descripcion
                }
                id_type.create(new_record)
            for id_ty in id_type.search([]):
                print(id_ty.description)

    def sync_document_sec_type(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTipoDocumentoSector(
            **params)

        if (ambiente == 1):
            document_sec_type = self.env['document_sec_type']
            document_sec_type.search([]).unlink()
            print(document_sec_type.search([]))
            for doc_sec_type in result.listaCodigos:
                new_record = {
                    'code': doc_sec_type.codigoClasificador,
                    'description': doc_sec_type.descripcion
                }
                document_sec_type.create(new_record)
            for doc_sec in document_sec_type.search([]):
                print(doc_sec.description)
    
    def sync_emission_types(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTipoEmision(
            **params)

        if (ambiente == 1):
            emission_types = self.env['emission_types']
            emission_types.search([]).unlink()
            print(emission_types.search([]))
            for emission_type in result.listaCodigos:
                new_record = {
                    'id_emission_type': emission_type.codigoClasificador,
                    'description': emission_type.descripcion
                }
                emission_types.create(new_record)
            for doc_sec in emission_types.search([]):
                print(doc_sec.description)
    
    def sync_room_types(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTipoHabitacion(
            **params)

        # if (ambiente == 1):
        #     emission_types = self.env['emission_types']
        #     emission_types.search([]).unlink()
        #     print(emission_types.search([]))
        #     for emission_type in result.listaCodigos:
        #         new_record = {
        #             'id_emission_type': emission_type.codigoClasificador,
        #             'description': emission_type.descripcion
        #         }
        #         emission_types.create(new_record)
        #     for doc_sec in emission_types.search([]):
        #         print(doc_sec.description)

    def sync_payment_methods(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTipoMetodoPago(
            **params)

        # if (ambiente == 1):
        #     payment_methods = self.env['payment_methods']
        #     payment_methods.search([]).unlink()
        #     print(payment_methods.search([]))
        #     for emission_type in result.listaCodigos:
        #         new_record = {
        #             'id_emission_type': emission_type.codigoClasificador,
        #             'description': emission_type.descripcion
        #         }
        #         payment_methods.create(new_record)
        #     for doc_sec in payment_methods.search([]):
        #         print(doc_sec.description)
    
    def sync_currency_types(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTipoMoneda(
            **params)

        # if (ambiente == 1):
        #     payment_methods = self.env['payment_methods']
        #     payment_methods.search([]).unlink()
        #     print(payment_methods.search([]))
        #     for emission_type in result.listaCodigos:
        #         new_record = {
        #             'id_emission_type': emission_type.codigoClasificador,
        #             'description': emission_type.descripcion
        #         }
        #         payment_methods.create(new_record)
        #     for doc_sec in payment_methods.search([]):
        #         print(doc_sec.description)

    def sync_selling_point_types(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTipoPuntoVenta(
            **params)

        # if (ambiente == 1):
        #     payment_methods = self.env['payment_methods']
        #     payment_methods.search([]).unlink()
        #     print(payment_methods.search([]))
        #     for emission_type in result.listaCodigos:
        #         new_record = {
        #             'id_emission_type': emission_type.codigoClasificador,
        #             'description': emission_type.descripcion
        #         }
        #         payment_methods.create(new_record)
        #     for doc_sec in payment_methods.search([]):
        #         print(doc_sec.description)

    def sync_invoice_types(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaTiposFactura(
            **params)

        # if (ambiente == 1):
        #     payment_methods = self.env['payment_methods']
        #     payment_methods.search([]).unlink()
        #     print(payment_methods.search([]))
        #     for emission_type in result.listaCodigos:
        #         new_record = {
        #             'id_emission_type': emission_type.codigoClasificador,
        #             'description': emission_type.descripcion
        #         }
        #         payment_methods.create(new_record)
        #     for doc_sec in payment_methods.search([]):
        #         print(doc_sec.description)
    
    def sync_measure_unit(self, ws_method):
        client = ws_method['client']
        params = ws_method['params']
        ambiente = int(ws_method['ambience'])
        result = client.service.sincronizarParametricaUnidadMedida(
            **params)

        if (ambiente == 1):
            measure_unit = self.env['measure_unit']
            measure_unit.search([]).unlink()
            print(measure_unit.search([]))
            for measure in result.listaCodigos:
                new_record = {
                    'measure_unit_code': measure.codigoClasificador,
                    'description': measure.descripcion
                }
                measure_unit.create(new_record)
            for measure in measure_unit.search([]):
                print(measure.description)
    
    def verifica_nit(self,  ambience, code_modality, system_code, branch_office, cuis, nit, nit_to_verify):
        
        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_obt_cod(),
            settings=settings)
        params = {'SolicitudVerificarNit': {
            'codigoAmbiente': ambience,
            'codigoModalidad': code_modality,
            'codigoSistema': system_code,
            'codigoSucursal': branch_office,
            'cuis': cuis,
            'nit': nit,
            'nitParaVerificacion': nit_to_verify
            }
        }
        result = client.service.verificarNit(**params)
        return result
        
        

    # Métodos de Facturacion Electrónica

    def send_invoice(self, emission_type, ambience, code_modality, selling_point, system_code, branch_office, cuis, nit, cufd, xml_file, xml_hash, date):
        code_doc_sec = '1'
        invoice_type = '1'
        # date = str(self.env['account.move'].getTime().strftime(
        #     "%Y-%m-%dT%H:%M:%S.%f"))

        # date = self.env['account.move'].req_sync_datetime()

        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_comp_vent(),
            settings=settings)
        params = {'SolicitudServicioRecepcionFactura': {
            'codigoAmbiente': ambience,
            'codigoDocumentoSector': code_doc_sec,
            'codigoEmision': emission_type,
            'codigoModalidad': code_modality,
            'codigoPuntoVenta': selling_point,
            'codigoSistema': system_code,
            'codigoSucursal': branch_office,
            'cufd': cufd,
            'cuis': cuis,
            'nit': nit,
            'tipoFacturaDocumento': invoice_type,
            'archivo': xml_file,
            # Omitir ultimos 3 dígitos de los microsegundos
            'fechaEnvio': date,
            # 'fechaEnvio': str(date[:-6]) + '000',
            'hashArchivo': xml_hash
        }
        }
        print(str(params))
        result = client.service.recepcionFactura(**params)
        print(result)
        return result

    def sign_xml(self, xml, credentials_path, pk, cert, signed_path):
        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl='http://190.181.63.219:8080/FirmaDigital/FirmaDigital?wsdl', ## Externo
            # wsdl='http://10.1.4.163:8080/FirmaDigital/FirmaDigital?wsdl', ## Alpha Interno
            settings=settings)

        params = {
            'arg0': str(xml),
            'arg1': credentials_path,
            'arg2': pk,
            'arg3': cert,
            'arg4': signed_path
        }

        # print(str(params))

        result = client.service.firmarXML(**params)
        return result

    def cancel_invoice(self, cuf, cufd, reason_code, id_ambience, id_sector_type, id_emission, id_modality, id_selling_point, system_code, id_branch_office, cuis):
        
        nit = str(self.env.company.vat)
        invoice_type = '1'
        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_comp_vent(),
            settings=settings)
        params = {'SolicitudServicioAnulacionFactura': {
            'codigoAmbiente': id_ambience,
            'codigoDocumentoSector': id_sector_type,
            'codigoEmision': id_emission,
            'codigoModalidad': id_modality,
            'codigoPuntoVenta': id_selling_point,
            'codigoSistema': system_code,
            'codigoSucursal': id_branch_office,
            'cufd': cufd,
            'cuis': cuis,
            'nit': nit,
            'tipoFacturaDocumento': invoice_type,
            'codigoMotivo': str(reason_code),
            'cuf': cuf
            }
        }
        print(str(params))
        result = client.service.anulacionFactura(**params)
        print(result)
        return result

    # Método de consumo Certificación Catalogos

    def cert_sync_catal(self, iterations, sellingPoint):
        ambience = str(self.env['ambience'].search(
            [('description', '=', 'PRUEBAS')]).id_ambience)
        selling_point = str(sellingPoint)
        branch_office = str(self.env['branch_office'].search(
            [('description', '=', 'CASA MATRIZ')]).id_branch_office)
        system_code = str(self.env['bo_edi_params'].search(
            [('name', '=', 'CODIGOSISTEMA')]).value)
        cuis = ''
        if (sellingPoint == 0):
            cuis = str(self.env['bo_edi_params'].search(
                [('name', '=', 'CUIS-0')]).value)
        elif (sellingPoint == 1):
            cuis = str(self.env['bo_edi_params'].search(
                [('name', '=', 'CUIS-1')]).value)
        nit = str(self.env['bo_edi_params'].search(
            [('name', '=', 'NIT')]).value)

        ws_method_sync = self.sync_general(ambience,
                                            selling_point,
                                            system_code,
                                            branch_office,
                                            cuis,
                                            nit)

        for i in range(iterations):
            self.sync_measure_unit(
                ws_method_sync
            )
        print('Prueba Finalizada')

    # Métodos de Eventos Significativos

    def send_invoice_event(self, ambiente,  puntoventa, codSistema, codSucursal, cuis, nit, cufd,codigoMotivoEvento,descripcion,fechaInicioEvento,fechaFinEvento,cufdEvento):
        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_op(),
            settings=settings)
        params = {'SolicitudEventoSignificativo': {
            'codigoAmbiente': ambiente,
            'codigoSistema': codSistema,
            'nit': nit,
            'cuis': cuis,
            'cufd': cufd,
            'codigoSucursal': codSucursal,
            'codigoPuntoVenta': puntoventa,
            'codigoMotivoEvento': codigoMotivoEvento,
            'descripcion': descripcion,
            'fechaHoraInicioEvento': fechaInicioEvento,
            'fechaHoraFinEvento': fechaFinEvento,
            'cufdEvento': cufdEvento        
        }
        }
        _logger.info("---------------- ENVIO DE EVENTO SIG -----------------")
        _logger.info(" REQUEST EVENTO SIG: " + str(params))
        result = client.service.registroEventoSignificativo(**params)
        _logger.info(" RESPUESTA ENVIO DE EVENTO SIG: " + str(result))
        _logger.info("------------------------------------------------------")
        return result.codigoRecepcionEventoSignificativo
   
    def conexion(self):
        resp=False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
           s.connect(("www.google.com", 80))
        except (socket.gaierror, socket.timeout):
            print("Sin conexión a internet")
        else:
            print("Con conexión a internet")
            resp=True
        s.close()        
        return resp

    def send_package(self,cufd, pack_content, pack_hash, cafc, inv_quantity, event_code,
                     id_modality, id_ambience, selling_point, branch_office, system_code,
                     cuis, nit):
        code_doc_sec = '1'
        code_emission_type = '2'
        invoice_type = '1'
        date = str(self.env['account.move'].getTime().strftime(
            "%Y-%m-%dT%H:%M:%S.%f"))

        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_comp_vent(),
            settings=settings)

        if not cafc:
                params = {'SolicitudServicioRecepcionPaquete': {
                'codigoAmbiente': id_ambience,
                'codigoDocumentoSector': code_doc_sec,
                'codigoEmision': code_emission_type,
                'codigoModalidad': id_modality,
                'codigoPuntoVenta': selling_point,
                'codigoSistema': system_code,
                'codigoSucursal': branch_office,
                'cufd': cufd,
                'cuis': cuis,
                'nit': nit,
                'tipoFacturaDocumento': invoice_type,
                'archivo': pack_content,
                'fechaEnvio': str(date[:-6]) + '000',
                'hashArchivo': pack_hash,
                'cantidadFacturas': inv_quantity,
                'codigoEvento':event_code
                }
            }
        else:
            params = {'SolicitudServicioRecepcionPaquete': {
                'codigoAmbiente': id_ambience,
                'codigoDocumentoSector': code_doc_sec,
                'codigoEmision': code_emission_type,
                'codigoModalidad': id_modality,
                'codigoPuntoVenta': selling_point,
                'codigoSistema': system_code,
                'codigoSucursal': branch_office,
                'cufd': cufd,
                'cuis': cuis,
                'nit': nit,
                'tipoFacturaDocumento': invoice_type,
                'archivo': pack_content,
                'fechaEnvio': str(date[:-6]) + '000',
                'hashArchivo': pack_hash,
                'cafc': cafc,
                'cantidadFacturas': inv_quantity,
                'codigoEvento':event_code
                }
            }
        _logger.info("---------------- ENVIO DE PAQUETE -----------------")
        _logger.info(" REQUEST ENVIO PAQUETE: " + str(params))
        result = client.service.recepcionPaqueteFactura(**params)
        _logger.info(" RESPUESTA ENVIO PAQUETE: " + str(result))
        _logger.info("----------------------------------------------------")
        print(result)

        return result

    def verify_package(self, ambiente,  puntoventa, codSucursal, codModalidad,
                        codSistema, cuis, nit, cufd, codeRecept):

        token = self.get_token().token
        settings = zeep.Settings(
            extra_http_headers={'apikey': str(token)})
        client = zeep.Client(
            wsdl= self._get_url_comp_vent(),
            settings=settings)
        params = {'SolicitudServicioValidacionRecepcionPaquete': {
            'codigoAmbiente': ambiente,
            'codigoDocumentoSector': '1',
            'codigoEmision': '2',
            'codigoModalidad': codModalidad,
            'codigoPuntoVenta': puntoventa,
            'codigoSistema': codSistema,
            'codigoSucursal': codSucursal,
            'cufd': cufd,
            'cuis': cuis,
            'codigoRecepcion':codeRecept,
            'nit': nit,
            'tipoFacturaDocumento': '1',
            }
        }
        _logger.info("---------------- VERIFICACION DE PAQUETE -----------------")
        _logger.info(" REQUEST VERIFICACION PAQUETE: " + str(params))
        result = client.service.validacionRecepcionPaqueteFactura(**params)
        _logger.info(" RESPUESTA VERIFICACION PAQUETE: " + str(result))
        _logger.info("----------------------------------------------------------")
        print(result)
        
        return result

        
