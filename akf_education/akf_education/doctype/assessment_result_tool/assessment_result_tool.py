# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AssessmentResultTool(Document):
	
	@frappe.whitelist()
	def get_latest_checked_enrollment(self):
		prog_enrollment = frappe.get_all(
			"Program Enrollment",
			filters={
				"student": self.student_id,
				"latest": 1,
				"docstatus": 1
			},
			fields=["name", "program", "academic_year","latest"],
			order_by="creation desc",
			limit=1
		)
		# frappe.throw(f"Program Enrollment: {prog_enrollment}")
		return prog_enrollment

	@frappe.whitelist()
	def get_courses(self):
		if self.current_program_enrollment:
			courses = frappe.get_all('Program Enrollment Course', filters={'parent': self.current_program_enrollment}, fields=['course'])
			# frappe.throw(f"Courses: {courses}")
			return courses
		else:
			return []
	
	@frappe.whitelist()
	def generate_assessment_result(self):
		if not self.current_program_enrollment:
			frappe.throw("No program enrollment found for the student.")
		
		courses = self.get_courses()
		if not courses:
			frappe.throw("No courses found for the current program enrollment.")
		
		assessment_result = frappe.new_doc("Assessment Result")
		assessment_result.student = self.student_id
		assessment_result.program = self.program
		assessment_result.details = self.details
		assessment_result.academic_year = self.academic_year
		assessment_result.save(ignore_permissions=True)
		return assessment_result.name
		
