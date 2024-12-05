# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import SUPERUSER_ID, api


def uninstall_hook(cr, registry, vals=None):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref("account_payment_mode.account_payment_mode_menu").parent_id = env.ref("account.account_management_menu").id
