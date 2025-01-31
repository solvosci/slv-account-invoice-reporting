# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Account Invoice Report Show Picking",
    "summary": """
        Show on invoice reports the picking it comes from
    """,
    "author": "Solvos",
    "license": "AGPL-3",
    "version": "17.0.1.0.0",
    'category': "Accounting & Finance",
    "website": "https://github.com/solvosci/slv-account",
    "depends": ["stock_picking_invoice_link"],
    "data": [
        "reports/account_invoice_template.xml"
    ],
    'installable': True,
}
