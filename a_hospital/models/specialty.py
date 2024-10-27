from odoo import fields, models


class DoctorSpecialty(models.Model):
    """
    Model representing a specialty area for doctors within the hospital system.

    Specialties categorize doctors based on their area of expertise.

    Fields:
        - name (Char): Name of the specialty.
        - description (Text): Details about the specialty area.
    """
    _name = 'a_hospital.specialty'
    _description = 'Doctor Specialty'

    name = fields.Char(string="Specialty Name", required=True)
    description = fields.Text()
