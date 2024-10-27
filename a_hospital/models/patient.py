import logging
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class Patient(models.Model):
    """
    Model representing a patient in the hospital system.

    Each patient record includes basic personal and contact details,
    and fields for linking to their personal doctor, diagnosis history,
    and emergency contacts.

    Fields:
        - personal_doctor_id (Many2one): The assigned personal doctor
        of the patient.
        - birth_date (Date): Date of birth of the patient.
        - passport_details (Char): Passport or ID details of the patient.
        - contact_person (Char): Emergency contact for the patient.
        - age (Integer): Computed field representing the age of the patient.
        - disease_id (Many2one): Reference to the patient’s primary disease.
        - diagnosis_history_ids (One2many): History of diagnoses
        for the patient.
    """
    _inherit = 'a_hospital.person'
    _name = 'a_hospital.patient'
    _description = 'Patient'

    personal_doctor_id = fields.Many2one(
        comodel_name='a_hospital.doctor',
        string="Personal Doctor",
    )

    birth_date = fields.Date(string="Date of Birth")

    passport_details = fields.Char()

    contact_person = fields.Char(string="Emergency Contact")

    age = fields.Integer(
        compute='_compute_age',
        store=True,
    )

    disease_id = fields.Many2one(
        comodel_name='a_hospital.disease',
        string='Disease')

    doctor_id = fields.Many2one(
        comodel_name='a_hospital.doctor',
        string='Person doctor')

    diagnosis_history_ids = fields.One2many(
        comodel_name='a_hospital.diagnosis',
        inverse_name='patient_id',
        string="Diagnosis History"
    )

    def add_visit(self):
        """
        Opens a form to quickly create a visit for the patient.
        Returns:
            dict: Action to open the visit creation form.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quick create visit',
            'res_model': 'a_hospital.visit',
            'target': 'new',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_patient_id': self.id,
                'quick_create': True, },
        }

    @api.depends('birth_date')
    def _compute_age(self):
        """
        Calculates the age of the patient based on birth_date.
        """
        for record in self:
            if record.birth_date:
                record.age = relativedelta(
                    fields.Date.today(),
                    record.birth_date).years
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        """
        Logs the creation of a new patient record.
        """
        patient = super(Patient, self).create(vals)
        _logger.info(f"New patient created: "
                     f"{patient.first_name} {patient.last_name}, "
                     f"ID: {patient.id}")
        return patient

    def write(self, vals):
        """
        Logs updates made to the patient record.
        """
        result = super(Patient, self).write(vals)
        _logger.info(f"Patient updated: "
                     f"{self.first_name} {self.last_name}, "
                     f"ID: {self.id}")
        return result

    def open_patient_visit_act_window_calendar(self):
        """
        Opens a calendar view of the patient's visits filtered by their doctor.
        """
        action = {
            'name': 'Patient visit',
            'type': 'ir.actions.act_window',
            'res_model': 'a_hospital.visit',
            'domain': [('doctor_id', '=', self.personal_doctor_id.id)],
            'context': {
                'default_doctor_id': self.personal_doctor_id.id,
                'default_patient_id': self.id,
            },
            'view_mode': 'calendar',
            'view_id': self.env.ref('a_hospital.patient_visit_calendar').id,
        }
        return action

    def show_patient_visits(self):
        """
        Shows a list of all visits for the current patient.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Patient visits',
            'res_model': 'a_hospital.visit',
            'target': 'current',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [
                ["patient_id", "=", self.id],
            ],
        }
