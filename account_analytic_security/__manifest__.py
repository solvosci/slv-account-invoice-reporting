# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Analityc Security",
    "summary": """
        Add a new group and two registration rules to restrict users from creating or deleting analytical accounts
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "15.0.1.1.0",
    'category': "Accounting & Finance",
    "website": "https://github.com/solvosci/slv-account",
    "depends": ["analytic"],
    "data": [
        "security/account_security.xml",
        "views/analytic_account_views.xml",
    ],
    'installable': True,
}
