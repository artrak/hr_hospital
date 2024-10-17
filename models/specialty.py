from odoo import fields, models


class DoctorSpecialty(models.Model):
    _name = 'hr_hospital.specialty'
    _description = 'Doctor Specialty'

    name = fields.Char(string="Specialty Name", required=True)
    description = fields.Text()
