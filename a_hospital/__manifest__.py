{
    'name': 'Hospital Management by Artemius',
    'summary': 'Module to manage hospital records for doctors and patients',
    'author': 'Artemius',
    'website': 'https://github.com/artrak/a_hospital',
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
        'security/a_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/a_hospital_security.xml',

        'wizard/a_hospital_disease_report_wizard_views.xml',
        'wizard/a_hospital_mass_reassign_doctor_wizard_views.xml',

        'views/a_hospital_disease_views.xml',
        'views/a_hospital_diagnosis_views.xml',
        'views/a_hospital_specialty_views.xml',
        'views/a_hospital_doctor_views.xml',
        'views/a_hospital_patient_views.xml',
        'views/a_hospital_visit_views.xml',
        'views/a_hospital_menu.xml',

        'report/a_hospital_doctor_report.xml'

    ],
    'demo': [
        'demo/a_hospital_disease.xml',
        'demo/a_hospital_specialty.xml',
        'demo/a_hospital_doctor.xml',
        'demo/a_hospital_patient.xml',
        'demo/a_hospital_visit.xml',
        'demo/a_hospital_diagnosis.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
