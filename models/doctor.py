from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _


class Doctor(models.Model):
    _inherit = 'hr_hospital.person'
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

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

    intern_ids = fields.One2many(
        comodel_name='hr_hospital.doctor',
        inverse_name='mentor_id',
        string='Interns'
    )

    patient_ids = fields.One2many(
        comodel_name='hr_hospital.patient',
        inverse_name='doctor_id',
        string='Patients')

    # Забороняємо вибирати інтерна в якості ментора
    @api.constrains('mentor_id')
    def check_mentor(self):
        for doctor in self:
            if not doctor.mentor_id and doctor.is_intern:
                raise ValidationError(_(
                    "An intern cannot be selected as a mentor."))

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        for doctor in self:
            if doctor.is_intern:
                doctor.mentor_id = "False"
