# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_partner_id = fields.Many2one(
        comodel_name="res.partner",
        compute='_compute_payment_partner_id',
        store=True,
        readonly=False,
        states={
            'posted': [('readonly', True)],
            'sent': [('readonly', True)],
            'reconciled': [('readonly', True)],
            'cancelled': [('readonly', True)],          
        },
    )

    @api.depends('partner_id')
    def _compute_payment_partner_id(self):
        for record in self:
            record.payment_partner_id = record.partner_id
