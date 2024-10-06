from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'

    active = fields.Boolean(default=True)           # Поле для архівування

    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string='Patient',
        required=True,
    )

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
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
        comodel_name='hr_hospital.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses'
    )

    # Заборона змін для час/дата/лікаря візитів, які вже відбулися
    @api.onchange('visit_date', 'doctor_id', 'visit_status')
    def _onchange_visit_date(self):
        self.ensure_one()
        if self.visit_status == 'completed' and self.doctor_id.is_intern:
            raise ValidationError(_(
                "You cannot modify the scheduled date "
                "or doctor for a completed visit."))

    # Заборона видаляти візити з діагнозами.
    def unlink(self):
        for visit in self:
            if visit.diagnosis_ids:
                raise ValidationError(_("You cannot delete "
                                      "visits with diagnoses."))
            return super(Visit, self).unlink()  # Викликаємо super

    # Заборона архівувати візити з діагнозами.
    @api.constrains('active')
    def _check_active(self):
        for visit in self:
            if not visit.active and visit.diagnosis_ids:
                raise ValidationError(_("Visits with diagnoses "
                                      "cannot be archived. "
                                      "Please remove diagnoses "
                                      "before archiving."))

    # Блокувати, щоб не можна було записати одного пацієнта
    # до одного лікаря в один день більше одного разу.
    @api.constrains('patient_id', 'doctor_id', 'scheduled_date')
    def _check_duplicate_visit(self):
        for visit in self:
            existing_visits = self.env['hr_hospital.visit'].search_count([
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

    # Зберігаємо ім'я лікаря під час створення запису
    @api.model
    def create(self, vals):
        if 'doctor_id' in vals:
            doctor = self.env['hr_hospital.doctor'].browse(vals['doctor_id'])

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

    # Зберігаємо ім'я лікаря після вибору лікаря
    @api.constrains('doctor_id', 'visit_status')
    def _onchange_doctor_id(self):
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
                            "Doctor has already been approved for this visit."))
