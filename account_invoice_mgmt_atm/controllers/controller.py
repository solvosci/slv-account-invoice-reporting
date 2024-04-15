# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from odoo import http, _
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class AddonCajeroHttp(http.Controller):

    @http.route('/cajero/ConsultaReciclaje', type='http', auth='api_key', methods=['GET', 'POST'], csrf=False)
    def cajero_consulta_reciclaje(self, *args, **post):
        json_data = request.httprequest.data
        ret_code = 0
        price_subtotal = 0
        ret_name = ''
        ret_success = True
        json_data = json.loads(json_data.decode('utf-8'))
        invoice_id = request.env["account.move"].sudo().search([('encrypted_name_lower', '=', json_data["parCodigo"])])
        partner_id = request.env["res.partner"].sudo().search([('vat', '=', json_data["parNIF"])])

        # LISTA ERRORES "ret_code"
        # SIN_INCIDENCIA = 0,
        # EXCEPCION_EN_SERVER = 1,
        # NO_ORIGINAL = 2,
        # CADUCADO = 3,
        # SIN_DATOS = 4,
        # TITULO_YA_PAGADO = 5,
        # TITULO_NO_DEIXALLERIES = 6,
        # DNI_NO_COINCIDE = 7,
        # SIN_DATOS_LCB = 8,
        # NO_COINCIDE_CENTRO_ALBARAN = 9,
        # ALBARAN_BLOQUEADO = 11,

        if not invoice_id:
            ret_code = 9
            ret_success = False
        elif json_data["parNIF"] != "" and not partner_id:
            ret_code = 7
            ret_success = False
        elif (invoice_id.amount_residual) <= 0:
            ret_code = 5
            ret_success = False
        else:
            ret_name = invoice_id.partner_id.name
            price_subtotal = invoice_id.amount_residual * 100

        json_result = {
            'retAceptado': ret_success,
            'retCodigo': ret_code,
            'retImporte': round(price_subtotal),
            'retImporteEfectivo': 0,
            'retImporteCheque': 0,
            'retNombre': ret_name
        }
        return str(json_result)

    @http.route('/cajero/EmisionCompletadaReciclaje', type='http', auth='api_key', methods=['GET', 'POST'], csrf=False)
    def cajero_emision_completada_reciclaje(self, *args, **post):
        try:
            res_company_id = request.env["res.users"].browse(request.uid).company_id
            json_data = request.httprequest.data
            json_data = json.loads(json_data.decode('utf-8'))
            #region
            # POSTMAN
            # {
            #     "parCodigo":"BILL/2022/0009",
            #     "parImporte":5,
            #     "parCajero":0,
            #     "parFormaPago":0,
            #     "parNumeroCheque":121212,
            #     "parIdPago":"BILL/2022/0009/13:10/15:10"
            # }
            #endregion

            account_invoice_id = request.env["account.move"].sudo().search([('encrypted_name_lower', '=', json_data["parCodigo"])])
            amount = int(json_data["parImporte"])/100
            atm_id = json_data["parCajero"] #NU
            payment_type = json_data["parFormaPago"]
            payment_ATM_id = json_data["parIdPago"]
            check_number = json_data["parNumeroCheque"]

            vals = {}

            if not request.env["account.payment"].sudo().search([('payment_ATM_id', '=', payment_ATM_id)]):
                typeofMove = "outbound"
                vals.update({"partner_type": "supplier"})
                payment_method_id = res_company_id.sudo().journal_ATM_id.outbound_payment_method_ids[0]
                vals.update({
                    "atm_check": check_number,
                    "payment_type": typeofMove, #outbound
                    "payment_method_id": payment_method_id.id,
                    "amount": amount, #cantidad
                    "currency_id": res_company_id.currency_id.id, #outbound
                    "journal_id": res_company_id.journal_ATM_id.id, #Cash
                    "partner_id": account_invoice_id.partner_id.id, #Nicole
                    "communication": ('CAJERO-%s') % account_invoice_id.name, #Da un poco igual
                    "payment_ATM_id": payment_ATM_id, # Codigo cajero
                    "invoice_ids": [(4, account_invoice_id.id)] # Facturas relacionadas
                })
                account_payment_temp = request.env["account.payment"].sudo().create(vals)
                account_payment_temp.post()
                _logger.info(('ATM Payment successful: payment_id:%s invoice_id:%s quantity:%s') % (account_payment_temp.id, account_invoice_id.id, amount))
                return str({'retRegistro': True})
            else:
                _logger.warning(('ATM Payment failed alredy exist a payment_ATM_id: %s. It will be ignored') % (payment_ATM_id))
                return str({'retRegistro': True})
        except Exception as e:
            _logger.error(e)
            return str({'retRegistro': False})

    @http.route('/cajero/PING', type='http', methods=['GET', 'POST'], auth='api_key', csrf=False)
    def cajero_ping(self, *args, **post):
        return str({'retRegistro': True})
