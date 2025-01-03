# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    promissory_note_number = fields.Char(related='move_id.promissory_note_number')
