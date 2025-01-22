# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Move Report 80mm",
    "summary": """
        Adds new report in Account Move with Ticket format (80mm)
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "15.0.1.0.0",
    "category": "Invoicing",
    "website": "https://github.com/solvosci/slv-account",
    "depends": ["account"],
    "data": [
        "reports/account_move_report_80mm_report.xml",
        "reports/account_move_report_80mm_template.xml",
    ],
    "installable": True,
}
