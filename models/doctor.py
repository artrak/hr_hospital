from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    _inherit = 'hr_hospital.person'
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name', required=True)

    # specialty = fields.Char()

    specialty_id = fields.Many2one(
        comodel_name='hr_hospital.specialty',
        string="Specialty",
    )

    is_intern = fields.Boolean(string="Intern")

    mentor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)]
    )

    patient_ids = fields.One2many(
        comodel_name='hr_hospital.patient',
        inverse_name='doctor_id',
        string='Patients')

    # Забороняємо вибирати інтерна в якості ментора
    @api.constrains('mentor_id')
    def check_mentor(self):
        for doctor in self:
            if doctor.mentor_id and doctor.is_intern:
                raise ValidationError("An intern cannot be selected as a mentor.")


