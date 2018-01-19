# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class HrHolidaysStatus(models.Model):
    _inherit = "hr.holidays"

    number_of_days_temp_2 = fields.Float('Allocation')