# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AssessmentResultTool(Document):
	@frappe.whitelist()
	def get_courses(self):
		courses = []
		frappe.msgprint("worked")
