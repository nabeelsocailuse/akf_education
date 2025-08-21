# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class PromoteStudent(Document):
	@frappe.whitelist()
	def get_students(self):
		active_enrolled_students = frappe.qb.DocType("Program Enrollment")
		students = []
		students = (
					frappe.qb.from_(active_enrolled_students)
					.select(
						(active_enrolled_students.student).as_("student_id"),
						(active_enrolled_students.student_name).as_("student_name"),
						(active_enrolled_students.program).as_("program"),
						(active_enrolled_students.academic_year).as_("academic_year"),
						(active_enrolled_students.aghosh_home_id).as_("aghosh_home_id"),
						(active_enrolled_students.aghosh_home_name).as_("aghosh_home_name"),
						(active_enrolled_students.school_type).as_("school_type"),
						(active_enrolled_students.internal_school).as_("internal_school"),
						(active_enrolled_students.external_school).as_("external_school"),
						(active_enrolled_students.building).as_("building"),
						(active_enrolled_students.room).as_("room"),
						(active_enrolled_students.bed).as_("bed"),
					)
					.where(active_enrolled_students.active == 1)
					.where(active_enrolled_students.program == self.program)
					.where(active_enrolled_students.aghosh_home_id == self.aghosh_home_id)
					.where(active_enrolled_students.academic_year == self.academic_year)
					.where(active_enrolled_students.docstatus == 1)
				)
		students = students.run(as_dict=1)

		# frappe.throw(f"Students: {students}")
		if students:
			return students
		else:
			frappe.throw(_("No students Found"))

	@frappe.whitelist()
	def promote_students(self):
		# total = len(self.students)
		for i, stud in enumerate(self.students):
			prog_enrollment = frappe.new_doc("Program Enrollment")
			prog_enrollment.student = stud.student_id
			prog_enrollment.student_name = stud.student_name
			prog_enrollment.program = self.new_program
			prog_enrollment.academic_year = self.new_academic_year
			prog_enrollment.aghosh_home_id = self.aghosh_home_id
			prog_enrollment.school_type = stud.school_type
			prog_enrollment.building = stud.building
			prog_enrollment.room = stud.room
			prog_enrollment.bed = stud.bed
			prog_enrollment.external_school = stud.external_school
			prog_enrollment.internal_school = stud.internal_school
			prog_enrollment.save()
