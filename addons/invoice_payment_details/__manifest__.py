# -*- coding: utf-8 -*-
{
    'name': 'Invoice Payment History',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Show payment history details on invoices',
    'description': """
        Invoice Payment History Module
        Энэ модуль нь дараах функцүүдийг нэмнэ:
        * Нэхэмжлэхийн жагсаалт дээр "Төлөгдсөн дүн" багана
        * Төлбөрийн түүхийг харуулах "Дэлгэрэнгүй" товч
        * Popup цонхонд төлбөрийн дэлгэрэнгүй мэдээлэл
        * Зөвхөн Ерөнхий нягтлан бодогчид хандах эрх
        * PDF тайланд төлбөрийн мэдээлэл (Bonus)
    """,
    'author': 'Munkhtur',
    'website': 'https://www.yourcompany.com',
    'depends': ['account', 'base'],
    'data': [
        'views/account_move_views.xml',
        'views/wizard_views.xml',
        'views/report_invoice.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False, 
    'license': 'LGPL-3',
}