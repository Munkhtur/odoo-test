# from odoo import models, fields

# class PaymentHistoryWizard(models.TransientModel):
#     _name = 'payment.history.wizard'
#     _description = 'Invoice Payment History'

#     invoice_id = fields.Many2one('account.move', string='Invoice')
#     payment_ids = fields.Many2many('account.payment', string='Payments', compute='_compute_payments')

#     def _compute_payments(self):
#         for wiz in self:
#             wiz.payment_ids = wiz.invoice_id.payment_ids

from odoo import api, fields, models

class PaymentHistoryWizard(models.TransientModel):
    _name = 'account.payment.history.wizard'
    _description = 'Invoice Payment History Wizard'

    invoice_id = fields.Many2one('account.move', string='Invoice', required=True)
    payment_line_ids = fields.One2many('account.payment.history.line', 'wizard_id', string='Payments')

    def _prepare_lines(self, invoice):
        lines = []
        payments = self.env['account.payment'].search([('invoice_ids', 'in', invoice.id)], order='payment_date asc')
        for p in payments:
            lines.append((0, 0, {
                'payment_date': p.payment_date,
                'amount': p.amount,
                'journal_id': p.journal_id.id,
                'communication': p.communication or p.name or '',
            }))
        return lines

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        invoice = self.env['account.move'].browse(self.env.context.get('active_id')) if self.env.context.get('active_id') else None
        if invoice and invoice.exists():
            res['invoice_id'] = invoice.id
            res['payment_line_ids'] = self._prepare_lines(invoice)
        return res

    def action_open(self):
        # Just used to open wizard (no server-side changes)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment.history.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

class PaymentHistoryLine(models.TransientModel):
    _name = 'account.payment.history.line'
    _description = 'Payment history line'
    wizard_id = fields.Many2one('account.payment.history.wizard', ondelete='cascade')
    payment_date = fields.Date('Payment Date')
    amount = fields.Monetary('Amount', currency_field='currency_id')
    journal_id = fields.Many2one('account.journal', 'Journal')
    communication = fields.Char('Memo')
    currency_id = fields.Many2one('res.currency', related='wizard_id.invoice_id.currency_id', store=False)
