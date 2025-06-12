# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import nowdate
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import today


class StudentAdmission(WebsiteGenerator):
	def autoname(self):
		if not self.title:
			self.title = self.get_title()
		self.name = self.title

	def validate(self):
		if self.admission_start_date and self.admission_end_date < today():
			frappe.throw("Date must be today or later.")

		if not self.route:  # pylint: disable=E0203
			self.route = "admissions/" + "-".join(self.title.split(" "))

		if self.enable_admission_application and not self.program_details:
			frappe.throw(_("Please add programs to enable admission application."))

	def get_context(self, context):
		context.no_cache = 1
		context.show_sidebar = True
		context.title = self.title
		context.parents = [
			{"name": "admissions", "title": _("All Student Admissions"), "route": "admissions"}
		]

	def get_title(self):
		return _("Admissions for {0}").format(self.academic_year)


def get_list_context(context=None):
	context.update(
		{
			"show_sidebar": True,
			"title": _("Student Admissions"),
			"get_list": get_admission_list,
			"row_template": "akf_education/doctype/student_admission/templates/student_admission_row.html",
		}
	)

def get_admission_list(
	doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified"
):
	return frappe.db.sql(
		"""
    SELECT sa.name, sa.title, sa.academic_year, sa.modified, sa.admission_start_date, 
           sa.route, sa.admission_end_date,sa.aghosh_home_id, sa.aghosh_home_name, sad.program, sad.min_age, sad.max_age, sad.description
    FROM `tabStudent Admission` sa
    LEFT JOIN `tabStudent Admission Program` sad ON sad.parent = sa.name
    WHERE sa.published = 1 AND sa.admission_end_date >= %s
    ORDER BY sa.admission_end_date ASC
    LIMIT {0}, {1}
    """.format(limit_start, limit_page_length),
    [nowdate()],
    as_dict=1,
	)
