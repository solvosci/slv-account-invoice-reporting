# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Payment Promissory Note Partner Address",
    "summary": """
        Allows to add payment partner address to promissory note."
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "13.0.1.0.0",
    'category': "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_check_printing_report_base",
    ],
    "data": [
        "views/account_payment_views.xml",
        "report/payment_partner_address_template.xml",
    ],
    'installable': True,
}
