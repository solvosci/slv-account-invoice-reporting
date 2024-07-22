# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import SUPERUSER_ID, api


def uninstall_hook(cr, registry, vals=None):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref("account_analytic_default.menu_analytic_default_list").parent_id = env.ref("account.menu_analytic_accounting").id
