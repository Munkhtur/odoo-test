# addons/invoice_payment_details/data/hooks.py
import logging
from odoo import api, SUPERUSER_ID
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

def _create_demo_data(cr, registry):
    """Create demo invoices and payments for a test customer."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    try:
        # Find the demo data records created by XML
        demo_customer = env.ref('invoice_payment_details.res_partner_demo_customer')
        invoice_1 = env.ref('invoice_payment_details.invoice_1')
        invoice_2 = env.ref('invoice_payment_details.invoice_2')

        # Post the invoices to confirm them
        invoice_1.action_post()
        invoice_2.action_post()

        _logger.info("Demo invoices posted.")

        # Create 5 payments for the first invoice
        for i in range(5):
            payment = env['account.payment'].create({
                'amount': 100.0 * (i + 1),
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': demo_customer.id,
                'date': datetime.now() - timedelta(days=5-i),
                'ref': f'Payment for Invoice 1 - Part {i+1}',
            })
            payment.action_post()
            # Reconcile payment with the invoice
            lines = (payment.line_ids + invoice_1.line_ids).filtered(
                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled
            )
            lines.reconcile()
            _logger.info(f"Created and reconciled payment {i+1} for Invoice 1.")

        # Create 5 payments for the second invoice
        for i in range(5):
            payment = env['account.payment'].create({
                'amount': 200.0 * (i + 1),
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': demo_customer.id,
                'date': datetime.now() - timedelta(days=5-i),
                'ref': f'Payment for Invoice 2 - Part {i+1}',
            })
            payment.action_post()
            # Reconcile payment with the invoice
            lines = (payment.line_ids + invoice_2.line_ids).filtered(
                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled
            )
            lines.reconcile()
            _logger.info(f"Created and reconciled payment {i+1} for Invoice 2.")

        _logger.info("Odoo demo data creation hook executed successfully.")

    except Exception as e:
        _logger.error(f"Failed to create Odoo demo data: {e}")

