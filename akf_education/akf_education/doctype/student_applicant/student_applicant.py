# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_years, date_diff, getdate, nowdate


class StudentApplicant(Document):
	def autoname(self):
		from frappe.model.naming import set_name_by_naming_series

		if self.student_admission:
			naming_series = None
			if self.program:
				# set the naming series from the student admission if provided.
				student_admission = get_student_admission_data(self.student_admission, self.program)
				if student_admission:
					naming_series = student_admission.get("applicant_naming_series")
				else:
					naming_series = None
			else:
				frappe.throw(_("Select the program first"))

			if naming_series:
				self.naming_series = naming_series

		set_name_by_naming_series(self)
	
	# def before_save(self):
	# 	self.create_or_update_guardian()
  
	def on_update(self):
		self.create_or_update_guardian()
		

	def validate(self):
		self.set_title()
		self.validate_dates()
		self.validate_term()

		if self.student_admission and self.program and self.date_of_birth:
			self.validation_from_student_admission()

	def set_title(self):
		self.title = " ".join(
			filter(None, [self.first_name, self.middle_name, self.last_name])
		)

	def validate_dates(self):
		if self.date_of_birth and getdate(self.date_of_birth) >= getdate():
			frappe.throw(_("Date of Birth cannot be greater than today."))

	def validate_term(self):
		if self.academic_year and self.academic_term:
			actual_academic_year = frappe.db.get_value(
				"Academic Term", self.academic_term, "academic_year"
			)
			if actual_academic_year != self.academic_year:
				frappe.throw(
					_("Academic Term {0} does not belong to Academic Year {1}").format(
						self.academic_term, self.academic_year
					)
				)

	def validation_from_student_admission(self):

		student_admission = get_student_admission_data(self.student_admission, self.program)

		if (
			student_admission
			and student_admission.min_age
			and date_diff(
				nowdate(), add_years(getdate(self.date_of_birth), student_admission.min_age)
			)
			< 0
		):
			frappe.throw(
				_("Not eligible for the admission in this program as per Date Of Birth")
			)

		if (
			student_admission
			and student_admission.max_age
			and date_diff(
				nowdate(), add_years(getdate(self.date_of_birth), student_admission.max_age)
			)
			> 0
		):
			frappe.throw(
				_("Not eligible for the admission in this program as per Date Of Birth")
			)
   

	def on_payment_authorized(self, *args, **kwargs):
		self.db_set("paid", 1)


	def create_or_update_guardian(self):
		# Try to fetch an existing Guardian linked to this Student Applicant
		guardian_doc = frappe.get_all(
			"Guardian",
			filters={"student_applicant": self.name},
			fields=["name"]
		)

		if guardian_doc:
			# Guardian exists - update it
			guardian = frappe.get_doc("Guardian", guardian_doc[0].name)
			guardian.guardian_name = self.name5
			guardian.gender_guardian = self.gender_guardian
			guardian.address = self.address
			guardian.relation_with_child = self.relation_with_child
			guardian.occupation_details = self.occupation_details
			guardian.education = self.education
			guardian.marital_status = self.marital_status
			guardian.mobile_number = self.contact_number
			guardian.save(ignore_permissions=True)
			frappe.msgprint(f"Guardian {guardian.name} updated for student {self.name}")
		else:
			# Guardian doesn't exist - create new one
			guardian = frappe.new_doc("Guardian")
			guardian.guardian_name = self.name5
			guardian.gender_guardian = self.gender_guardian
			guardian.address = self.address
			guardian.relation_with_child = self.relation_with_child
			guardian.occupation_details = self.occupation_details
			guardian.education = self.education
			guardian.marital_status = self.marital_status
			guardian.mobile_number = self.contact_number
			guardian.student_applicant = self.name
			guardian.insert(ignore_permissions=True)
			guardian.save()
			frappe.msgprint(f"Guardian {guardian.name} created for student {self.name}")
		
		        
         
    

def get_student_admission_data(student_admission, program):

	admission_programs = frappe.get_all(
		"Student Admission Program",
		{"parenttype": "Student Admission", "parent": student_admission, "program": program},
		["applicant_naming_series", "min_age", "max_age"],
	)

	if admission_programs:
		return admission_programs[0]
	return None
