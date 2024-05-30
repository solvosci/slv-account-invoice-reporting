import logging
from openupgradelib import openupgrade  # pylint: disable=W7936


@openupgrade.migrate()
def migrate(env, version):
    logging.getLogger('odoo.addons.account_invoice_mgmt_dms').info(
        'Recalculating with_doc flag for'
        ' stock moves linked to dms files')
    directory_id = env.ref('account_invoice_mgmt_dms.dms_directory_carrier_doc', raise_if_not_found=False)
    # for dms_file in env["dms.file"].search([('directory_id', '=', directory_id.id), ('proceeding', '!=', False)]):
    #     env["stock.move"].search([('picking_id.name', '=', dms_file.proceeding)]).with_doc = True
    openupgrade.logged_query(
        env.cr,
        f"""
        UPDATE
            stock_move
        SET
            with_doc = true
        FROM
            stock_move sm
        INNER JOIN
            stock_picking sp on sp.id=sm.picking_id
        INNER JOIN
            dms_file df on df.proceeding=sp.name
            and df.directory_id = {directory_id.id}
        WHERE
            stock_move.id=sm.id
        ;""",
    )
