# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Financial Report Menu",
    "summary": """
        Change the menu position "Invoicing/Reports/OCA accounting reports" to "Invoicing/OCA accounting reports"
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_financial_report",
    ],
    "data": [
        "views/account_financial_report_menu.xml",
    ],
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
