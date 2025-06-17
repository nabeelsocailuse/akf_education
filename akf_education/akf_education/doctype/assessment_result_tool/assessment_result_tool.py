# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from frappe.model.document import Document

class AssessmentResultTool(Document):
	def validate_marks(self):
		for row in self.details:
			if not row.score or not row.maximum_score:
				frappe.throw(
					_(f"Marks cannot be empty in row#{row.idx}. Please enter a valid marks value.")
				)
				
			if row.score and row.maximum_score < 0:
				frappe.throw(
					_(f"Marks cannot be negative in row#{row.idx}. Please enter a valid marks value.")
				)

			if row.score and row.maximum_score > 100:
				frappe.throw(
					_(f"Marks cannot exceed 100 in row#{row.idx}. Please enter a valid marks value.")
				)

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
		self.validate_marks()
		if not self.current_program_enrollment:
			frappe.throw("No program enrollment found for the student.")
		
		courses = self.get_courses()
		if not courses:
			frappe.throw("No courses found for the current program enrollment.")
		
		assessment_result = frappe.new_doc("Assessment Result")
		assessment_result.student = self.student_id
		assessment_result.program = self.program
		assessment_result.details = self.details
		assessment_result.select_term = self.select_term
		assessment_result.academic_year = self.academic_year
		assessment_result.save(ignore_permissions=True)
		return assessment_result.name
		
