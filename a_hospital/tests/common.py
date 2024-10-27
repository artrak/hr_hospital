from datetime import datetime

from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()

        # Створення спеціальностей
        self.specialty_cardiology = self.env['a_hospital.specialty'].create({
            'name': 'Cardiology',
            'description': 'Specialized in heart diseases'
        })

        # Створення лікаря-ментора
        self.doctor_mentor = self.env['a_hospital.doctor'].create({
            'first_name': 'Dmytro',
            'last_name': 'Shevchenko',
            'specialty_id': self.specialty_cardiology.id,
            'is_intern': False,
            'gender': 'male',
        })

        # Створення інтерна з ментором
        self.intern_doctor = self.env['a_hospital.doctor'].create({
            'first_name': 'Intern',
            'last_name': 'Ivanov',
            'specialty_id': self.specialty_cardiology.id,
            'is_intern': True,
            'mentor_id': self.doctor_mentor.id,
            'gender': 'male',
        })

        # Створення пацієнта
        self.patient = self.env['a_hospital.patient'].create({
            'first_name': 'Ivan',
            'last_name': 'Petrov',
            'birth_date': '1990-01-01',
            'personal_doctor_id': self.doctor_mentor.id,
            'gender': 'male',
        })

        # Створення типу хвороби та хвороби
        self.disease_type_infectious = (
            self.env['a_hospital.disease.type'].create({
                'name': 'Infectious',
                'description': 'Infectious diseases'
            })
        )

        self.disease_flu = self.env['a_hospital.disease'].create({
            'name': 'Flu',
            'disease_type_id': self.disease_type_infectious.id,
        })

        # Створення візиту пацієнта
        self.visit = self.env['a_hospital.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.intern_doctor.id,
            'scheduled_date': datetime.now(),
            'visit_status': 'scheduled',
        })

        # Створення діагнозу
        self.diagnosis = self.env['a_hospital.diagnosis'].create({
            'visit_id': self.visit.id,
            'doctor_id': self.intern_doctor.id,
            'disease_id': self.disease_flu.id,
            'patient_id': self.patient.id,
            'is_approved': False,
        })
