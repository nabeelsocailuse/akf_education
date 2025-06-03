# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AssessmentResultTool(Document):
	
	@frappe.whitelist()
	def get_latest_checked_enrollment(self):
		# enrollment = frappe.db.get_value(
		# 	"Program Enrollment",
		# 	{
		# 		"student": self.student_id,
		# 		"latest": 1,
		# 		"docstatus": 1,
		# 	},
		# 	["name", "program", "academic_year"]
		# )
		# return enrollment[0] if enrollment else None
		return frappe.get_all(
        "Program Enrollment",
        filters={"student": self.student_id, "latest": 1},
        fields=["name", "program", "academic_year"],
        order_by="creation desc",
        limit=1
    )

	@frappe.whitelist()
	def get_courses(self):
		courses = []
		frappe.msgprint("worked")
