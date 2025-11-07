# Invoice Payment Details Module - Odoo 16 Docker Setup

## Steps:

1. Clone the repository.
2. Run:
   docker-compose up -d
3. cat backup.sql | docker exec -i odoo-test-db-1 psql -U odoo -d postgres
3. Open http://localhost:8069

Login Credentials
| Field    | Value      |
| -------- | ---------- |
| Email    | admin@mail |
| Password | admin      |
