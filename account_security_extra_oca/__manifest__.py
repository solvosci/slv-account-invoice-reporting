# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Security Extra",
    "summary": """
        - Change the menu position "Invoicing/Configuration/Payment Mode" to "Invoicing/Accounting/Payment Mode"
        - In group Account User adds write and create permission to account.payment.mode
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "13.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_payment_mode",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_security_extra_oca_menu.xml",
    ],
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
