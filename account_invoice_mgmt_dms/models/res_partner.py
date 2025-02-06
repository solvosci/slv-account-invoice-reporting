# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 (https://www.gnu.org/licenses/lgpl-3.0.html)

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    validator_complete_proceesing_id = fields.Many2one(
        comodel_name='res.users',
        string='Default Document Validator',
        domain=lambda self: self._get_group_invoice_validator(),
    )

    @api.model
    def _get_group_invoice_validator(self):
        group = self.env.ref('account_invoice_mgmt_dms.group_invoice_validator', raise_if_not_found=False)
        if group:
            return [('groups_id', 'in', group.id)]
        return []
