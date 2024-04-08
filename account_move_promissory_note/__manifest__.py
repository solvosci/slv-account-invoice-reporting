# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Move Promissory Note",
    "summary": """
        Adds promissory note in account move tree view
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "13.0.1.2.0",
    'category': "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_payment_promissory_note_number",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    'installable': True,
}
