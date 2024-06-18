from odoo import models, fields

class AccountJournal(models.Model):
    _inherit="account.journal"
    
    name = fields.Char(tracking=True)
    code = fields.Char(tracking=True)
    currency_id = fields.Many2one(tracking=True)
    default_account_id = fields.Many2one(tracking=True)
