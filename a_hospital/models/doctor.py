from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _


class Doctor(models.Model):
    """
    Model representing a doctor in the hospital system.

    Doctors can be interns or experienced practitioners with specialties.
    Interns must be supervised by a mentor doctor, and each doctor may have
    multiple interns assigned under their mentorship.

    Fields:
        - specialty_id (Many2one): The specialty area of the doctor.
        - is_intern (Boolean): Indicates if the doctor is an intern.
        - mentor_id (Many2one): Reference to the mentor doctor.
        - intern_ids (One2many): List of interns assigned to this doctor
        as a mentor.
        - patient_ids (One2many): List of patients under
        the care of this doctor.
    """
    _inherit = 'a_hospital.person'
    _name = 'a_hospital.doctor'
    _description = 'Doctor'

    specialty_id = fields.Many2one(
        comodel_name='a_hospital.specialty',
        string="Specialty",
    )

    is_intern = fields.Boolean(string="Intern")

    mentor_id = fields.Many2one(
        comodel_name='a_hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)]
    )

    intern_ids = fields.One2many(
        comodel_name='a_hospital.doctor',
        inverse_name='mentor_id',
        string='Interns'
    )

    patient_ids = fields.One2many(
        comodel_name='a_hospital.patient',
        inverse_name='doctor_id',
        string='Patients')

    @api.constrains('mentor_id')
    def check_mentor(self):
        """
        Ensures that only a non-intern doctor can be assigned as a mentor.
        Raises:
            ValidationError: If an intern is selected as a mentor.
        """
        for doctor in self:
            if not doctor.mentor_id and doctor.is_intern:
                raise ValidationError(_(
                    "An intern cannot be selected as a mentor."))

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        """
        Clears the mentor field if the doctor is an intern.
        """
        for doctor in self:
            if doctor.is_intern:
                doctor.mentor_id = "False"
