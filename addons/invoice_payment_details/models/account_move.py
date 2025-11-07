from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_paid = fields.Monetary(
        string='Төлөгдсөн дүн',
        compute='_compute_amount_paid',
        currency_field='currency_id',
        store=True
    )

    @api.depends('payment_state', 'line_ids.matched_debit_ids', 'line_ids.matched_credit_ids')
    def _compute_amount_paid(self):
        for move in self:
            print(move)
            paid = 0
            for payment in move._get_reconciled_info_JSON():
                paid += payment.get('amount', 0)
            move.amount_paid = paid
