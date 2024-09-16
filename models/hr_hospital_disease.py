from odoo import models, fields

class Disease(models.Model):
    _name = 'hr_hospital2.disease'
    _description = 'Disease'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
