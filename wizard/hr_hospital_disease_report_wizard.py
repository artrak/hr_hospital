from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'hr_hospital.disease.report.wizard'
    _description = 'Description'

    name = fields.Char()
