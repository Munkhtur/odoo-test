from odoo import models, fields, api

class InvoicePaymentWizard(models.TransientModel):
    _name = 'invoice.payment.wizard'
    _description = 'Invoice Payment History Wizard'

    move_id = fields.Many2one('account.move', required=True, ondelete='cascade')
    payment_line_ids = fields.One2many('invoice.payment.line', 'wizard_id')

    def _get_payment_lines(self):
        lines = []
        payments = self.move_id._get_reconciled_payments().filtered(lambda p: p.state == 'posted')
        for pay in payments:
            lines.append((0, 0, {
                'payment_date': pay.payment_date,
                'amount': pay.amount,
                'journal_id': pay.journal_id.id,
                'ref': pay.ref or pay.name,
            }))
        return lines


    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        move_id = self.env.context.get('default_move_id')
        if move_id:
            move = self.env['account.move'].browse(move_id)
            res['move_id'] = move.id
            res['payment_line_ids'] = self._get_payment_lines()
        return res


class InvoicePaymentLine(models.TransientModel):
    _name = 'invoice.payment.line'
    _description = 'Payment Line'

    wizard_id = fields.Many2one('invoice.payment.wizard', ondelete='cascade')
    payment_date = fields.Date()
    amount = fields.Monetary(currency_field='currency_id')
    journal_id = fields.Many2one('account.journal')
    ref = fields.Char()
    currency_id = fields.Many2one(related='wizard_id.move_id.currency_id')
