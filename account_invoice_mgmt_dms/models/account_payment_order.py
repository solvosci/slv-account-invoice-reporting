# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import _, models
from odoo.exceptions import ValidationError


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"


    def generated2uploaded(self):
        pending_invoice_ids = self.payment_line_ids.move_line_id.move_id.filtered(lambda x: x.state_complete_proceesing in ['pending', 'validated', 'declined'])
        requires_invoice_approval = self.payment_line_ids.move_line_id.move_id.filtered(lambda x: not x.payment_mode_id.skip_invoice_approval)
        if pending_invoice_ids and requires_invoice_approval:
            raise ValidationError(
                    _("Before making payment, the following invoices must be approved: %s") % (', '.join(invoice.name for invoice in pending_invoice_ids))
                )
        return super(AccountPaymentOrder, self).generated2uploaded()
