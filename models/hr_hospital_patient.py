from odoo import models, fields

class Patient(models.Model):
    _name = 'hr_hospital2.patient'
    _description = 'Patient'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    disease_id = fields.Many2one('hr_hospital2.disease', string='Disease')
    doctor_id = fields.Many2one('hr_hospital2.doctor', string='Doctor')
