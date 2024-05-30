# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields, _


class AccountMoveDmsFileWizard(models.TransientModel):
    _name = 'stock.move.dms.file.wizard'
    _description = 'stock.move.dms.file.wizard'

    ticket_name = fields.Char()
    stock_move_id = fields.Many2one('stock.move')
    dms_file = fields.Binary("Attachment")
    dms_file_name = fields.Char()

    def link_stock_move_dms(self):
        directory_id = self.env.ref('account_invoice_mgmt_dms.dms_directory_carrier_doc')
        extension_name = self.dms_file_name.split(".")[-1]
        extension_size = -(len(extension_name)) - 1
        name = self.dms_file_name[:extension_size]
        # self.env['dms.file'].search([('proceeding', '=', self.ticket_name), ('directory_id', '=', directory_id.id)]).unlink()
        self.env['dms.file'].sudo().create({
            'name': '%s_%s.%s' % (name, (self.stock_move_id.picking_id.name).replace("/", ""), extension_name),
            'content': self.dms_file,
            'directory_id': directory_id.id,
            'proceeding': self.ticket_name,
        })
        self.stock_move_id.with_doc = True
