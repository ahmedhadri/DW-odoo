# -*- coding: utf-8 -*-
# module template
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR DigitalWorks',
    'version': '10.0',
    'category': 'HR',
    'license': 'AGPL-3',
    'author': "Ghandi Mouad & HADRI Ahmed",
    'website': 'https://www.odoo.com/',
    'depends': ['hr_payroll','l10n_ma_hr_payroll_10Basic'],
    'images': ['images/digital_works_logo.png'],
    'data': [
             'security/hr_payslip_security.xml',
             'views/hr_view.xml',
             'views/l10n_ma_hr_digitalworks_view.xml',
             'data/hr_employee_sequence.xml',
             'data/hr_payroll_extra_rules.xml',
             'data/wage_precision.xml',
             'data/wage_precision.xml',
             ],
    'installable': True,
    'application': True,
}
