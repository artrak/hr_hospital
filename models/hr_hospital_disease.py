from odoo import models, fields


class Disease(models.Model):

    name = fields.Char(
        required=True)
    description = fields.Text()
