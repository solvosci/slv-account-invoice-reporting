# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields, _


class AccountMoveAssignMasiveConfirmWizard(models.TransientModel):
    _name = 'account.move.assign.massive.confirm.wizard'
    _description = 'account.move.assign.massive.confirm.wizard'

    invoice_ids = fields.Many2many('account.move', readonly=1)

    def approve(self):
        for record in self.invoice_ids:
            record.complete_proceesing_id.approve_account_move()
