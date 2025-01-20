# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Move Payment Mode Editable",
    "summary": """
        Allow editing field mode in account.move in any case
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "13.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_payment_partner",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
}
