# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    carrier_doc_count = fields.Integer(compute="_compute_carrier_doc_count")
    dms_file_ids = fields.Many2many("dms.file",compute="_compute_carrier_doc_count")

    def _compute_carrier_doc_count(self):
        directory_id = self.env.ref("account_invoice_mgmt_dms.dms_directory_carrier_doc").id
        for record in self:
            record.carrier_doc_count = len(self.env['dms.file'].search([("proceeding", "=", record.picking_id.name), ("directory_id", "=", directory_id)]))
            record.dms_file_ids = self.env["dms.file"].search([("proceeding","=",record.picking_id.name),("directory_id", "=", directory_id)])

    def open_wizard_dms_file(self):
        Wizard = self.env['stock.move.dms.file.wizard']
        new = Wizard.create({
            'ticket_name': self.picking_id.name,
            'stock_move_id': self.id,
        })
        return {
            'name': _('Link Scale Weight with DMS'),
            'res_model': 'stock.move.dms.file.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': new.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def get_related_dms(self):
        directory_id = self.env.ref("account_invoice_mgmt_dms.dms_directory_carrier_doc").id
        dms_file_ids = self.env['dms.file'].search([("proceeding", "=", self.picking_id.name), ("directory_id", "=", directory_id)])
        action = {
            'name': _('Carrier Doc'),
            'res_model': 'dms.file',
            'target': 'current',
            'type': 'ir.actions.act_window',
        }
        if len(dms_file_ids) > 1:
            action['view_mode'] = 'tree,form'
            action['view_type'] = 'tree,form'
            action['res_id'] = dms_file_ids.ids
            action['domain'] = [('id', 'in', dms_file_ids.ids)]
        else:
            action['view_mode'] = 'form'
            action['view_type'] = 'form'
            action['res_id'] = dms_file_ids.id
        return action
