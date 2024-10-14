from odoo import models, fields


class DiseaseType(models.Model):
    _name = 'hr_hospital.disease.type'
    _description = 'Disease Type'

    name = fields.Char(string="Type Name", required=True)
    description = fields.Text(  )

    disease_ids = fields.One2many(
        comodel_name='hr_hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )
