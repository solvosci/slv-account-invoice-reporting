# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'

    skip_invoice_approval = fields.Boolean()
