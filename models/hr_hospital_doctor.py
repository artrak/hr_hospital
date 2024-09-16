from odoo import models, fields

class Doctor(models.Model):
    _name = 'hr_hospital2.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name', required=True)
    specialty = fields.Char(string='Specialty')
    patient_ids = fields.One2many('hr_hospital2.patient', 'doctor_id', string='Patients')
