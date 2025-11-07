# Invoice Payment Details Module - Odoo 16 Docker Setup

## Steps:

1. Clone the repository.
2. Run:
   docker-compose up -d
3. Open http://localhost:8069
4. Create a new database:
   - Master password: admin
   - Database name: odoo
   - Email: admin@mail.com
   - Password: admin
5. Go to Apps → Update Apps List → Install 'Invoice Payment Details'
6. Demo customer, invoices, and payments will be loaded automatically.
7. Use 'Дэлгэрэнгүй' button on invoices to see payment history.
