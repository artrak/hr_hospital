from odoo import models, fields


class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(
        string='Name',
        required=True)
    specialty = fields.Char(
        string='Specialty')
    patient_ids = fields.One2many(
        comodel_name='hr_hospital.patient',
        inverse_name='doctor_id',
        string='Patients')
