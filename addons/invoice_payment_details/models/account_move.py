# models/account_move.py
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_paid = fields.Monetary(
        string='Төлөгдсөн дүн',
        compute='_compute_amount_paid',
        store=False,
        currency_field='currency_id',
    )

    @api.depends('amount_total', 'amount_residual', 'move_type')
    def _compute_amount_paid(self):
        for move in self:
            if move.is_invoice(include_receipts=True):
                # Only for customer invoices/refunds
                move.amount_paid = move.amount_total - move.amount_residual
            else:
                move.amount_paid = 0.0
    

    def action_open_payment_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'invoice.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_move_id': self.id},
        }