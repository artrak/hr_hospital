from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _


class Diagnosis(models.Model):
    """
    Model representing a diagnosis within the hospital system.

    Each diagnosis is linked to a specific visit, doctor, patient,
    and disease, with an option for approval by a mentor doctor if
    the diagnosing doctor is an intern.

    Fields:
        - visit_id (Many2one): Reference to the visit in which the diagnosis
        was made.
        - doctor_id (Many2one): Reference to the doctor who made the diagnosis.
        - disease_id (Many2one): Reference to the diagnosed disease.
        - patient_id (Many2one): Reference to the patient who received
        the diagnosis.
        - description (Text): Additional information or notes regarding
        the diagnosis.
        - is_approved (Boolean): Indicates if the diagnosis was approved
        by a mentor doctor.
        - doctor_approved (Char): Name of the mentor doctor who approved
        the diagnosis.
        - disease_type_id (Many2one): Related field showing
        the type of the diagnosed disease.
    """
    _name = 'a_hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='a_hospital.visit',
        string='Visit',
        required=True,
    )

    doctor_id = fields.Many2one(
        comodel_name='a_hospital.doctor',
        string='Doctor',
        required=True
    )

    disease_id = fields.Many2one(
        comodel_name='a_hospital.disease',
        string='Disease',
        required=True
    )

    patient_id = fields.Many2one(
        comodel_name='a_hospital.patient',
        string='Patient',
        required=True,
    )

    description = fields.Text()

    is_approved = fields.Boolean(
        string='Approved',
        default=False,
        help="""This sign indicates that the given diagnosis,
                made by the mentor doctor,
                has been verified and approved by his mentor."""
    )

    doctor_approved = fields.Char(
        string='Doctor approved'
    )

    disease_type_id = fields.Many2one(
        related='disease_id.disease_type_id',
        comodel_name='a_hospital.disease.type',
        string='Disease Type',
        store=True,
        readonly=True
    )

    @api.constrains('visit_id', 'is_approved')
    def _check_approval_for_intern(self):
        """
        Ensures that diagnoses made by interns require mentor approval.
        Raises:
            ValidationError: If the intern’s diagnosis is not approved.
        """
        for diagnosis in self:
            doctor = diagnosis.visit_id.doctor_id
            if doctor.is_intern and diagnosis.is_approved:
                raise ValidationError(_(
                    "Diagnosis made by an intern must be approved "
                    "by the mentor."))

    @api.model
    def create(self, vals):
        """
        Ensures that diagnoses made by interns require mentor approval.
        Raises:
            ValidationError: If the intern’s diagnosis is not approved.
        """
        if 'visit_id' in vals:
            visit = self.env['a_hospital.visit'].browse(vals['visit_id'])
            vals['patient_id'] = visit.patient_id.id
        return super(Diagnosis, self).create(vals)

    @api.onchange('visit_id')
    def _onchange_visit_id(self):
        """
        Updates the patient_id based on the selected visit.
        """
        for patient in self:
            patient.patient_id = patient.visit_id.patient_id
