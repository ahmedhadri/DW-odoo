# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays"

    number_of_days_temp_2 = fields.Float('Allocation')

    # @api.model
    # def _automatique_leave_alloc(self):
    #     employee_ids = self.env['hr.employee'].search([('name', '=', 'AAJOUR Sara')])
    #     holiday_types = self.env['hr.holidays.status'].search([])
    #     print "Hehhooooo I am In _automatique_leave_alloc "
    #     for emplyee in employee_ids:
    #         vals = {
    #             'name': 'Automatique Leave 2017',
    #             'type': 'add',
    #             'holiday_type': 'employee',
    #             'holiday_status_id': holiday_types[0].id,
    #             'employee': emplyee.id,
    #             'remaining_leaves': 1.5,
    #         }
    #         self.create(vals)
    #     return True

class HrHolidaysLeaves(models.Model):
    _inherit = "hr.holidays.status"

    @api.multi
    def _dynamic_compute_leaves(self):
        employee_ids = self.env['hr.employee'].search([])
        for employee_id in employee_ids:
            legal_leave = employee_id.company_id.legal_holidays_status_id

            if employee_id.id:

                data_days = legal_leave.get_days(employee_id.id)

                result = data_days.get(legal_leave.id, {})
                # legal_leave.max_leaves = result.get('max_leaves', 0)
                # legal_leave.leaves_taken = result.get('leaves_taken', 0)
                legal_leave.remaining_leaves = result.get('remaining_leaves', 0)
                # legal_leave.virtual_remaining_leaves = result.get('virtual_remaining_leaves', 0)
                employee_id.remaining_leaves = legal_leave.remaining_leaves + 1.5

        return True