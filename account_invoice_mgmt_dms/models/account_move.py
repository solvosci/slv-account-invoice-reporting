# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import base64
import io
import ghostscript
import os
import tempfile


class AccountMove(models.Model):
    _inherit = 'account.move'

    ocr_doc = fields.Html(related='complete_proceesing_id.ocr_doc', store=True, readonly=True)
    dms_file_ids = fields.One2many('dms.file', 'account_move_id', readonly=True)
    dms_file_count = fields.Integer(compute='_compute_dms_file_count')

    purchase_invoice_proceesing_id = fields.Many2one('dms.file', compute='_compute_complete_proceesing_id', store=True, readonly=True)
    complete_proceesing_id = fields.Many2one('dms.file', compute='_compute_complete_proceesing_id', store=True, readonly=True)
    state_complete_proceesing = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    ], compute='_compute_state_complete_proceesing', store=True)
    decline_reason_complete_proceesing = fields.Char(related='complete_proceesing_id.decline_reason')
    rating_complete_proceesing = fields.Selection(related='complete_proceesing_id.rating', readonly=False)
    note_complete_proceesing = fields.Text(related='complete_proceesing_id.note', readonly=False)

    def _compute_dms_file_count(self):
        for record in self:
            record.dms_file_count = len(record.dms_file_ids)

    def _compute_ocr_doc(self):
        for record in self:
            if record.dms_file_ids:
                record.ocr_doc = record.complete_proceeding.ocr_doc
            else:
                record.ocr_doc = False

    @api.depends('complete_proceesing_id', 'complete_proceesing_id.state_account_move', 'reversed_entry_id.complete_proceesing_id.state_account_move')
    def _compute_state_complete_proceesing(self):
        for record in self:
            if record.reversed_entry_id:
                record.state_complete_proceesing = record.reversed_entry_id.complete_proceesing_id.state_account_move
            else:
                record.state_complete_proceesing = record.complete_proceesing_id.state_account_move

    @api.depends('dms_file_ids')
    def _compute_complete_proceesing_id(self):
        directory_id = self.env.ref('account_invoice_mgmt_dms.dms_directory_puchase_invoice')
        for record in self:
            if record.dms_file_ids.filtered(lambda x: x.complete_proceeding):
                record.complete_proceesing_id = record.dms_file_ids.filtered(lambda x: x.complete_proceeding)

            purchase_invoice_file = record.dms_file_ids.filtered(lambda x: x.directory_id == directory_id)
            if purchase_invoice_file:
                record.purchase_invoice_proceesing_id = purchase_invoice_file

    def action_dms_files(self):
        ticket_name = self.name
        directory_id = self.env.ref('account_invoice_mgmt_dms.dms_directory_extra_doc')
        for purchase_order_id in self.invoice_line_ids.purchase_line_id.order_id:
            ticket_name = self.env["stock.picking.classification"].sudo().search([("picking_id.classification_purchase_order_id", "=", purchase_order_id.id)]).picking_id.move_ids_without_package
        return {
            'name': _('DMS File'),
            'view_mode': 'tree,form',
            'res_model': 'dms.file',
            'type': 'ir.actions.act_window',
            'domain': [('account_move_id', '=', self.id)],
            'context': {'default_proceeding': ticket_name, 'default_directory_id': directory_id.id},
        }

    def open_wizard_dms(self, wizard_model):
        Wizard = self.env[wizard_model]
        new = Wizard.create({
            'account_move_id': self.id,
        })
        return {
            'res_model': wizard_model,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': new.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def open_wizard_dms_file(self):
        wizard = self.open_wizard_dms('account.move.dms.file.wizard')
        wizard['name'] = _('Add Partner Invoice')
        return wizard

    def open_wizard_dms_extra_file(self):
        wizard = self.open_wizard_dms('account.move.dms.extra.file.wizard')
        wizard['name'] = _('Add Extra Docs')
        return wizard
    
    def validation_files(self, dms_file):
        error = ''            
        try:
            self.env['ir.actions.report']._merge_pdfs([io.BytesIO(dms_file.content_binary)])
        except Exception as e:
            error = '\n - %s' % dms_file.name
        return error

    def create_dms_file_document_manager(self):
        validate = self.env.context.get('create_dms_file_document_validate',False)
        directory_id = self.env.ref('account_invoice_mgmt_dms.dms_directory_complete_proceeding')
        # invoice_pdf = io.BytesIO(self.env.ref("account.account_invoices").render_qweb_pdf(self.id)[0])

        proceeding = ''
        streams = []
        error = ''
        dms_file_purchase_invoice = self.dms_file_ids.filtered(lambda x: x.directory_id.id == self.env.ref('account_invoice_mgmt_dms.dms_directory_puchase_invoice').id)
        if dms_file_purchase_invoice:
            streams.append(io.BytesIO(dms_file_purchase_invoice.content_binary))
            if validate:
                error += self.validation_files(dms_file_purchase_invoice)

        # streams.append(invoice_pdf)
        for purchase_order_id in self.invoice_line_ids.purchase_line_id.order_id:
            ticket_id = self.env["stock.picking.classification"].sudo().search([("picking_id.classification_purchase_order_id", "=", purchase_order_id.id)]).picking_id.move_ids_without_package

            purchase_vp_pdf = io.BytesIO(self.env.ref("reports_alu.action_report_purchase_order_alumisel_vp").render_qweb_pdf(purchase_order_id.id)[0])
            streams.append(purchase_vp_pdf)

            if ticket_id:
                proceeding = ticket_id.picking_id.name
                ticket_pdf = io.BytesIO(self.env.ref("stock_picking_mgmt_weight.action_report_move_tag").render_qweb_pdf(ticket_id.id)[0])
                streams.append(ticket_pdf)

            dms_file_carrier_ids = self.env['dms.file'].sudo().search([('proceeding', '=', proceeding), ('directory_id', '=', self.env.ref('account_invoice_mgmt_dms.dms_directory_carrier_doc').id)])
            if dms_file_carrier_ids:
                for doc_carrier in dms_file_carrier_ids:
                    streams.append(io.BytesIO(doc_carrier.content_binary))
                    if validate:
                        error += self.validation_files(doc_carrier)

        if not proceeding:
            proceeding = self.name
        dms_extra_ids = self.env['dms.file'].sudo().search([('proceeding', 'ilike', proceeding), ('directory_id', '=', self.env.ref('account_invoice_mgmt_dms.dms_directory_extra_doc').id)])
        if dms_extra_ids:
            for doc_extra in dms_extra_ids:
                streams.append(io.BytesIO(doc_extra.content_binary))
                if validate:
                    error += self.validation_files(doc_extra)

        if self.complete_proceesing_id:
            self.complete_proceesing_id.unlink()

        if error:
            raise ValidationError(_("Error in files: %s \n Must uploaded again") % error)
        
        attachment = self.env['ir.actions.report']._merge_pdfs(streams)

        # Save the PDF to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf.write(attachment)
            temp_pdf_path = temp_pdf.name

        # Compress PDF using Ghostscript
        # https://ghostscript.readthedocs.io/en/gs10.04.0/VectorDevices.html
        compressed_pdf_path = temp_pdf_path.replace('.pdf', '_compressed.pdf')
        args = [
            "ps2pdf",
            "-dNOPAUSE", "-dBATCH", "-dSAFER","-dPDFSETTINGS=/ebook",
            "-sDEVICE=pdfwrite",
            "-sOutputFile=" + compressed_pdf_path,
            temp_pdf_path
        ]
        ghostscript.Ghostscript(*args)

        # Read the compressed PDF and encode it in base64
        with open(compressed_pdf_path, 'rb') as f:
            encoded_content = base64.b64encode(f.read())

        self.env['dms.file'].create({
            'name': 'DOC_%s.pdf' % (self.name).replace("/", ""),
            'content': encoded_content,
            'directory_id': directory_id.id,
            'proceeding': proceeding,
            'account_move_id': self.id,
            'state_account_move': 'pending',
            'complete_proceeding': True,
        })

        # Cleaning temporary files
        os.remove(temp_pdf_path)
        os.remove(compressed_pdf_path)

    def action_invoice_register_payment(self):
        if self.state_complete_proceesing in ['pending', 'declined']:
            raise ValidationError(
                    _("Must be approved before making payment")
                )
        return super(AccountMove, self).action_invoice_register_payment()

    def action_approve_complete_processing(self):
        if not self.env.user.has_group("account_invoice_mgmt_dms.group_invoice_approver"):
            raise ValidationError(_("You don't have permission to approve invoices."))

        active_ids = self.env["account.move"].browse(self._context.get("active_ids", []))
        invoice_ids = active_ids.filtered(lambda x: x.complete_proceesing_id and x.complete_proceesing_id.state_account_move == 'pending')

        Wizard = self.env['account.move.assign.massive.confirm.wizard']
        new = Wizard.create({
            'invoice_ids': invoice_ids,
        })
        return {
            'name': _('Are you sure you want to approve the following invoices?'),
            'res_model': 'account.move.assign.massive.confirm.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': new.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    
    def action_download_document(self,field_name,url_field):
        invoice_ids = self.env['account.move'].browse(self._context.get("active_ids", [])).filtered(lambda x: getattr(x, field_name))
        invoice_ids = [str(id) for id in invoice_ids.ids]
        if invoice_ids:
            url = '/account_invoice_mgmt_dms/%s?ids=%s' % (url_field,','.join(invoice_ids))
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }
        else:
            raise ValidationError(
                    _("No selected invoice has the supplier invoice stored")
                )
        
    def action_download_purchase_invoice(self):
        return self.action_download_document('purchase_invoice_proceesing_id', 'download_purchase_invoice')
    
    def action_download_complete_proceesing(self):
        return self.action_download_document('complete_proceesing_id', 'download_complete_proceesing')

