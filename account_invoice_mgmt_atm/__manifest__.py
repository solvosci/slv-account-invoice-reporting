# © 2022 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Invoice Mgmt Atm",
    "summary": """
        Adds communication between a cashier and the invoices, to make payments automatically
    """,
    "author": "Solvos",
    "license": "LGPL-3",
    "version": "13.0.1.2.1",
    "category": "stock",
    "website": "https://github.com/solvosci/slv-account",
    "depends": [
        "stock",
        "purchase",
        "account",
        "auth_api_key",
    ],
    "data": [
        "data/account_cash_rounding.xml",
        "reports/account_move_report.xml",
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
        "views/account_payment_views.xml",
        "views/purchase_order_view.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
}
