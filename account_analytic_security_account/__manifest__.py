# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Analityc Security Account",
    "summary": """
        Hide supplier invoices for certain users (those who are not invoicing users)
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "15.0.1.0.0",
    'category': "Accounting & Finance",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_analytic_security",
        "account",
        ],
    "data": [
        "views/analytic_account_views.xml",
    ],
    'installable': True,
}
