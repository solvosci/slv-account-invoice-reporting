# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import os


class DmsFile(models.Model):
    _inherit = "dms.file"

    account_move_id = fields.Many2one('account.move', string="Invoice Files")
    ocr_doc = fields.Html('Invoice Content', compute="_compute_ocr_doc", store=True, readonly=False)
    proceeding = fields.Char()
    rating = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'Hight'),
        ('3', 'Very Hight')
    ])
    note = fields.Text()
    state_account_move = fields.Selection([
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    ], string="Doc State", readonly=True)
    decline_reason = fields.Char()
    complete_proceeding = fields.Boolean(default=False)

    @api.depends('account_move_id.dms_file_ids.ocr_doc')
    def _compute_ocr_doc(self):
        directory_complete_proceeding_id = self.env.ref('account_invoice_mgmt_dms.dms_directory_complete_proceeding', raise_if_not_found=False)
        for record in self:
            if directory_complete_proceeding_id and record.directory_id == directory_complete_proceeding_id:
                dms_file_purchase_invoice = record.account_move_id.dms_file_ids.filtered(lambda x: x.id != record.id)
                record.ocr_doc = dms_file_purchase_invoice.ocr_doc

    def approve_account_move(self):
        self.state_account_move = 'approved'
        self.account_move_id.message_post(
            body=_("Approve Invoice")
        )
    
    def validate_account_move(self):
        for record in self:
            if not self.env.user.has_group("account_invoice_mgmt_dms.group_invoice_approver") and self.env.user.has_group("account_invoice_mgmt_dms.group_invoice_validator") and record.account_move_id.validator_complete_proceesing_id != self.env.user:
                raise ValidationError(_("You don't have permission to validate this invoice, only can validate the user: %s") % (record.account_move_id.validator_complete_proceesing_id.name))
            record.state_account_move = 'validated'
            record.account_move_id.message_post(
                body=_("Validate Invoice")
            )

    def decline_account_move(self):
        if self.state_account_move == 'validated' and not self.env.user.has_group("account_invoice_mgmt_dms.group_invoice_approver"):
            raise ValidationError(_("You don't have permission to decline this invoice."))
        if not self.env.user.has_group("account_invoice_mgmt_dms.group_invoice_approver") and self.env.user.has_group("account_invoice_mgmt_dms.group_invoice_validator") and self.account_move_id.validator_complete_proceesing_id != self.env.user:
            raise ValidationError(_("You don't have permission to decline this invoice."))
        Wizard = self.env['dms.file.decline.account.move.wizard']
        new = Wizard.create({
            'dms_file_id': self.id,
        })
        return {
            'name': _('Decline Purchase Invoice'),
            'res_model': 'dms.file.decline.account.move.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': new.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def unlink(self):
        directory_id = self.env.ref('account_invoice_mgmt_dms.dms_directory_carrier_doc', raise_if_not_found=False)
        if directory_id:
            for record in self.filtered(lambda x: x.directory_id == directory_id):
                move_id = self.env['stock.move'].sudo().search([('picking_id.name', '=', record.proceeding)])
                if move_id.carrier_doc_count == 1:
                    move_id.with_doc = False
        return super(DmsFile, self).unlink()

