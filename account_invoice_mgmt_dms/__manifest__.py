# © 2021 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html
{
    "name": "Account Invoice Management DMS",
    "summary": """
        Adds the possibility to read Invoice data from local to dms for bind and upload
    """,
    "version": "13.0.1.8.1",
    "category": "Accounting & Finance",
    "website": "https://github.com/solvosci/slv-account",
    "author": "Solvos",
    "license": "LGPL-3",
    "depends": [
        "account",
        "dms",
        "purchase",
        "stock_picking_mgmt_weight",
        "reports_alu",
        "account_due_list",
        "account_payment_order",
    ],
    "data": [
        "security/account_invoice_mgmt_dms_security.xml",
        "data/dms_access_group.xml",
        "data/dms_storage.xml",
        "data/dms_directory.xml",
        "views/stock_move_views.xml",
        "views/account_move_views.xml",
        "views/account_move_line_views.xml",
        "views/dms_file_view.xml",
        "views/purchase_order_views.xml",
        "wizards/stock_move_dms_file_wizard_view.xml",
        "wizards/account_move_dms_file_wizard_view.xml",
        "wizards/dms_file_decline_account_move_wizard_view.xml",
        "wizards/account_move_dms_extra_file_wizard_views.xml",
        "wizards/account_move_assign_massive_confirm_wizard_view.xml",
    ],
    "external_dependencies": {"python": ["pytesseract", "pdf2image", "ghostscript"]},
}
