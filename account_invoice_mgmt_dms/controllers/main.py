from odoo import http, _
from odoo.http import request
import base64
import io
import zipfile


class Binary(http.Controller):
    
    def _download_files(self, invoice_ids, file_field):
        invoice_ids = request.env['account.move'].browse(map(int, invoice_ids.split(',')))
        with io.BytesIO() as zip_buffer:
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for record in invoice_ids.filtered(lambda x: getattr(x, file_field)):
                    binary_data = getattr(record, file_field).content
                    decoded_data = base64.b64decode(binary_data)
                    file_name = record.name.replace("/", "_")
                    zip_file.writestr(f"{file_name}.pdf", decoded_data)

            zip_buffer.seek(0)
            zip_data = zip_buffer.read()

        return zip_data
    
    @http.route('/account_invoice_mgmt_dms/download_purchase_invoice', type='http', auth="user")
    def download_purchase_invoice(self, ids, **kw):
        return request.make_response(self._download_files(ids, 'purchase_invoice_proceesing_id'), [('Content-Type', 'application/zip'), ('Content-Disposition', 'attachment; filename=%s.zip' % _('invoice_files'))])

    @http.route('/account_invoice_mgmt_dms/download_complete_proceesing', type='http', auth="user")
    def download_complete_proceesing(self, ids, **kw):
        return request.make_response(self._download_files(ids, 'complete_proceesing_id'), [('Content-Type', 'application/zip'), ('Content-Disposition', 'attachment; filename=%s.zip' % _('complete_proceesing'))])

