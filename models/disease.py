from odoo import models, fields


class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char(required=True)
    description = fields.Text()
    parent_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Parent Disease'
    )
    child_ids = fields.One2many(
        comodel_name='hr_hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases'
    )
