# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Analytic Security Extra",
    "summary": """
        Change the menu position "Invoicing/Configuration/Analytic Defaults" to "Invoicing/Accounting/Management/Analytic Defaults"
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_analytic_default",
    ],
    "data": [
        "views/account_analytic_security_extra_menu.xml",
    ],
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
