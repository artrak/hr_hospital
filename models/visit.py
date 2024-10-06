from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'

    active = fields.Boolean(default=True)           # Поле для архівування

    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',         # Вказуємо модель, з якою є зв'язок
        string='Patient',
        required=True,
    )

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',          # Вказуємо модель, з якою є зв'язок
        string='Doctor',
        required=True,
    )

    visit_status = fields.Selection(
        [('scheduled', 'Scheduled'),
         ('completed', 'Completed'),
         ('canceled', 'Canceled')],
        string="Visit Status",
        required=True,
        default='scheduled',
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Date & Time",
        required=True,
    )

    visit_date = fields.Datetime(
        string="Visit Date & Time",
        required=True,
    )

    notes = fields.Text()

    diagnosis_ids = fields.One2many(
        comodel_name='hr_hospital.diagnosis',
        inverse_name='visit_id',                    # Має відповідати Many2one полю у моделі `Diagnosis`
        string='Diagnoses'
    )

    # Заборона змін для візитів, які вже відбулися
    @api.onchange('visit_date', 'doctor_id')
    def _onchange_visit_date(self):
        if self._origin:
            return {
                'warning': {
                    'title': "Warning",
                    'message': "You cannot modify the scheduled date or doctor for a completed visit."
                }
            }

    #Заборона видаляти візити з діагнозами.
    def unlink(self):
        for visit in self:
            if visit.diagnosis_ids:
                raise ValidationError("You cannot delete visits with diagnoses.")

    # Заборона архівувати візити з діагнозами.
    @api.constrains('active')
    def check_active(self):
        for visit in self:
            if not visit.active and visit.diagnosis_ids:
                raise ValidationError("You cannot archive visits with diagnoses.")

    #Перевірка на д самий день
    @api.constrains('patient_id', 'doctor_id', 'scheduled_date')
    def check_duplicate_visit(self):
        for visit in self:
            existing_visits = self.search([
                ('patient_id', '=', visit.patient_id.id),
                ('doctor_id', '=', visit.doctor_id.id),
                ('scheduled_date', '=', visit.scheduled_date),
                # ('id', '!=', visit.id),
            ])
            if existing_visits:
                raise ValidationError("A patient cannot have multiple visits with the same doctor on the same day.")

