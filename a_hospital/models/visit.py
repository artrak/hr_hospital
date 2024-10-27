import random
from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _


class Visit(models.Model):
    """
    Model representing a patient's visit within the hospital system.

    Visits are associated with patients, doctors, and may include diagnoses.
    This model supports tracking visit status, scheduling, and the assignment
    of doctors, including approvals by senior doctors.

    Fields:
        - patient_id (Many2one): The patient attending the visit.
        - doctor_id (Many2one): The doctor assigned to the visit.
        - initial_doctor_visit (Char): Initial doctor handling the visit.
        - doctor_approved (Char): Doctor who approved the visit, if required.
        - visit_status (Selection): Current status of the visit
        (e.g., scheduled, completed).
        - scheduled_date (Datetime): Scheduled date and time of the visit.
        - visit_date (Datetime): Actual date and time of the visit.
        - notes (Text): Additional notes about the visit.
        - diagnosis_ids (One2many): List of diagnoses made during the visit.
    """
    _name = 'a_hospital.visit'
    _description = 'Patient Visit'

    active = fields.Boolean(default=True)           # Поле для архівування

    patient_id = fields.Many2one(
        comodel_name='a_hospital.patient',
        string='Patient',
        required=True,
    )

    doctor_id = fields.Many2one(
        comodel_name='a_hospital.doctor',
        string='Doctor',
        required=True,
    )

    initial_doctor_visit = fields.Char(
        string="Initial doctor's visit",
        readonly=True,
    )

    doctor_approved = fields.Char(
        string='Doctor approved',
        readonly=True,
    )

    visit_status = fields.Selection(
        [('scheduled', 'Scheduled'),
         ('completed', 'Completed'),
         ('canceled', 'Canceled')],
        required=True,
        default='scheduled',
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Date & Time",
        required=True,
    )

    visit_date = fields.Datetime(
        string="Visit Date & Time",
    )

    notes = fields.Text()

    diagnosis_ids = fields.One2many(
        comodel_name='a_hospital.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses'
    )

    def generate_random_date(self):
        """
        Generates a random date within the next 30 days.
        Returns:
            str: Formatted random date and time string.
        """
        today = datetime.today()
        days_offset = random.randint(0, 30)
        random_date = today + timedelta(days=days_offset)
        return random_date.strftime('%Y-%m-%d %H:%M:%S')

    @api.onchange('visit_date', 'doctor_id', 'visit_status')
    def _onchange_visit_date(self):
        """
        Restricts modification of visit date, doctor, or status
        if the visit is completed and the doctor is an intern.
        Raises:
            ValidationError: If attempting to modify details
            of a completed visit.
        """
        self.ensure_one()
        if self.visit_status == 'completed' and self.doctor_id.is_intern:
            raise ValidationError(_(
                "You cannot modify the scheduled date "
                "or doctor for a completed visit."))

    def unlink(self):
        """
        Prevents deletion of visits that have associated diagnoses.
        Raises:
            ValidationError: If there are diagnoses linked to the visit.
        """
        for visit in self:
            if visit.diagnosis_ids:
                raise ValidationError(_("You cannot delete "
                                      "visits with diagnoses."))
            return super(Visit, self).unlink()  # Викликаємо super

    @api.constrains('active')
    def _check_active(self):
        """
        Restricts archiving visits that have diagnoses.
        Raises:
            ValidationError: If attempting to archive
            a visit with linked diagnoses.
        """
        for visit in self:
            if not visit.active and visit.diagnosis_ids:
                raise ValidationError(_(
                    "Visits with diagnoses cannot be archived. "
                    "Please remove diagnoses before archiving."
                ))

    @api.constrains('patient_id', 'doctor_id', 'scheduled_date')
    def _check_duplicate_visit(self):
        """
        Prevents scheduling multiple visits for the same patient
        with the same doctor on the same day.
        Raises:
            ValidationError: If there are duplicate visits on the same day.
        """
        for visit in self:
            existing_visits = self.env['a_hospital.visit'].search_count([
                ('patient_id', '=', visit.patient_id.id),
                ('doctor_id', '=', visit.doctor_id.id),
                ('scheduled_date', '>=', visit.scheduled_date.date()),
                ('scheduled_date', '<',
                 visit.scheduled_date.date() + timedelta(days=1)),
                ('id', '!=', visit.id)])
            if existing_visits != 0:
                raise ValidationError(_(
                    "A patient cannot have multiple visits "
                    "with the same doctor on the same day."))

    @api.model
    def create(self, vals):
        """
        Sets the initial doctor’s name if not provided and validates
        that an intern cannot be assigned as the initial doctor when
        the field is already populated.
        """
        if 'doctor_id' in vals:
            doctor = self.env['a_hospital.doctor'].browse(vals['doctor_id'])

            # Якщо лікар є інтерном і поле initial_doctor_visit
            # не пусте, забороняємо збереження
            if doctor.is_intern and vals.get('initial_doctor_visit'):
                raise ValidationError(_(
                    "An intern cannot be assigned as the initial doctor "
                    "when the field is already filled."))

            # Якщо поле initial_doctor_visit пусте,
            # записуємо ім'я лікаря в нього
            if not vals.get('initial_doctor_visit'):
                vals['initial_doctor_visit'] = doctor.display_name

        return super(Visit, self).create(vals)

    @api.constrains('doctor_id', 'visit_status')
    def _onchange_doctor_id(self):
        """
        Sets the doctor's name in the doctor_approved field once
        the visit is completed and approved.
        Raises:
            ValidationError: If attempting to re-approve
            an already approved visit.
        """
        for visit in self:
            if visit.doctor_id:
                doctor = visit.doctor_id

                # Якщо лікар не інтерн і візит завершений
                if not doctor.is_intern and visit.visit_status == 'completed':
                    # Перевірка, чи поле doctor_approved вже заповнено
                    if not visit.doctor_approved:  # Якщо порожнє або None
                        visit.doctor_approved = doctor.display_name
                    else:
                        raise ValidationError(_(
                            "Doctor has already been "
                            "approved for this visit."))
