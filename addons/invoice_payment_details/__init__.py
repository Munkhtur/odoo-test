from . import models
from . import wizard

from odoo import api, SUPERUSER_ID

def _post_init_hook_create_demo_data(cr, registry):
    from .data.hooks import _create_demo_data
    _create_demo_data(cr, registry)