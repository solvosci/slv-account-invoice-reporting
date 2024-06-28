# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Security Extra",
    "summary": """
        - Change the menu position "Invoicing/Configuration/Chart of Accounts" to "Invoicing/Accounting/Chart of Accounts"
        - In group Show Full Accounting Features adds write and create permission to account.account 
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_security_extra_menu.xml",
    ],
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
