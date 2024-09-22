{
    'name': 'Hospital Management',
    'summary': 'Module to manage hospital records for doctors and patients',
    'description': """
            Hospital Management Module
            - Manage Doctors
            - Manage Patients
            - Manage Diseases
            - Manage Visits
        """,
    'author': 'Artemius',
    'website': 'https://github.com/artrak/hr_hospital/',
    'category': 'Healthcare',
    'license': 'OPL-1',
    'version': '17.0.1.1.0',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_menu.xml',
    ],
    'demo': [
        'demo/hr_hospital_disease.xml',
        'demo/hr_hospital_doctor.xml',
        'demo/hr_hospital_patient.xml',
        'demo/hr_hospital_visit.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
