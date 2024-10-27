from datetime import datetime

from odoo.addons.a_hospital.tests.common import TestCommon
from odoo.exceptions import UserError


class TestAction(TestCommon):

    def test_01_action_compute_age(self):
        """Calculate expected age"""
        expected_age = datetime.now().year - 1990
        self.assertEqual(self.patient.age, expected_age,
                         "Age computation is incorrect")

    def test_02_action_constrains_scheduled(self):
        """Test that a patient cannot be scheduled for multiple visits to
        the same doctor on the same day."""
        with self.assertRaises(UserError):
            self.env['a_hospital.visit'].create({
                'patient_id': self.patient.id,
                'doctor_id': self.intern_doctor.id,
                'scheduled_date': self.visit.scheduled_date,
                'visit_status': 'scheduled',
            })

    def test_03_action_constrains_active(self):
        """Test that visits with diagnoses cannot be archived."""
        with self.assertRaises(UserError):
            self.visit.write({'active': False})

    def test_04_intern_cannot_approve_diagnosis(self):
        """Test that an intern cannot approve
        a diagnosis without mentor confirmation."""
        with self.assertRaises(UserError):
            self.diagnosis.write({'is_approved': True})

    def test_05_disease_hierarchy_complete_name(self):
        """Test that the complete name of a disease includes
        the parent's name."""
        parent_disease = self.env['a_hospital.disease'].create({
            'name': 'Respiratory Disease'
        })
        child_disease = self.env['a_hospital.disease'].create({
            'name': 'Pneumonia',
            'parent_id': parent_disease.id
        })
        self.assertEqual(child_disease.complete_name,
                         'Respiratory Disease / Pneumonia',
                         "Disease hierarchy complete name computation "
                         "is incorrect")
