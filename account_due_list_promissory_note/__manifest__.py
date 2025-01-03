# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Due List Promissory Note",
    "summary": """
        Adds promissory note in Payment and Due List view
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "13.0.1.0.0",
    'category': "Account",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "account_move_promissory_note",
        "account_due_list",
    ],
    "data": [
        "views/account_move_line_views.xml",
    ],
    'installable': True,
}
