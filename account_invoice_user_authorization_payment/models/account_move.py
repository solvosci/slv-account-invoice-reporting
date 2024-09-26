# © 2023 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import  models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    user_authorization_payment = fields.Many2one('res.users',
        compute='_compute_user_authorization_payment', store=True)

    @api.depends('payment_state')
    def _compute_user_authorization_payment(self):
        for move in self:
            if move.payment_state == 'paid':
                move.user_authorization_payment = self.env.user
