# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint
import json

from education.education.api import enroll_student

class ProgramEnrollmentTool(Document):
	def onload(self):
		academic_term_reqd = cint(frappe.db.get_single_value("Education Settings", "academic_term_reqd"))
		self.set_onload("academic_term_reqd", academic_term_reqd)  

	@frappe.whitelist()
	def get_students(self):
		students = []
		if not self.get_students_from:
			frappe.throw(_("Mandatory field - Get Students From"))
		elif not self.program:
			frappe.throw(_("Mandatory field - Program"))
		elif not self.academic_year:
			frappe.throw(_("Mandatory field - Academic Year"))
		elif not self.aghosh_home_id:
			frappe.throw ("Mandatory field - Aghosh Home")
   
		else:
			if self.get_students_from == "Student Applicant":
				student_applicant = frappe.qb.DocType("Student Applicant")

				students = (
					frappe.qb.from_(student_applicant)
					.select(
						(student_applicant.name).as_("student_applicant"),
						(student_applicant.title).as_("student_name"),
					)
					.where(student_applicant.application_status == "Approved")
					.where(student_applicant.program == self.program)
					.where(student_applicant.aghosh_home_id == self.aghosh_home_id)
					.where(student_applicant.academic_year == self.academic_year)
				)
				if self.academic_term:
					students = students.where(student_applicant.academic_term == self.academic_term)
				students = students.run(as_dict=1)

			elif self.get_students_from == "Program Enrollment":
				program_enrollment = frappe.qb.DocType("Program Enrollment")
				students = (
					frappe.qb.from_(program_enrollment)
					.select(
						program_enrollment.student,
						program_enrollment.student_name,
						program_enrollment.student_batch_name,
						program_enrollment.student_category,
					)
					.where(program_enrollment.program == self.program)
					.where(program_enrollment.academic_year == self.academic_year)
				)
				if self.academic_term:
					students = students.where(program_enrollment.academic_term == self.academic_term)
				if self.student_batch:
					students = students.where(
						program_enrollment.student_batch_name == self.student_batch
					)
				students = students.run(as_dict=1)

				student_list = [d.student for d in students]
				if student_list:
					inactive_students = frappe.db.sql(
						"""
						select name as student, student_name from `tabStudent` where name in (%s) and enabled = 0"""
						% ", ".join(["%s"] * len(student_list)),
						tuple(student_list),
						as_dict=1,
					)

					for student in students:
						if student.student in [d.student for d in inactive_students]:
							students.remove(student)

		if students:
			return students
		else:
			frappe.throw(_("No students Found"))
   
   
   
	@frappe.whitelist()
	def enroll_students(self):
		self.enrolled_students()
		self.create_sponsorships()

	def enrolled_students(self):
		# total = len(self.students)
		for i, stud in enumerate(self.students):
			if not stud.building:
				frappe.throw("please select building for the student first")
			if not stud.room:
				frappe.throw("please select room for the student first")
			if not stud.bed:
				frappe.throw("please select bed for the student first")
			if not stud.school_type:
				frappe.throw("Please select school type.")
			if stud.school_type == "Internal" and not stud.internal_school:
				frappe.throw("Internal School not selected.")
			if stud.school_type == "External" and not stud.external_school:
				frappe.throw("External School not selected.")
			
			# frappe.publish_realtime("program_enrollment_tool", dict(progress=[i + 1, total]), user=frappe.session.user)
			if stud.student:
				prog_enrollment = frappe.new_doc("Program Enrollment")
				prog_enrollment.student = stud.student
				prog_enrollment.student_name = stud.student_name
				prog_enrollment.student_category = stud.student_category
				prog_enrollment.program = self.new_program
				prog_enrollment.academic_year = self.new_academic_year
				prog_enrollment.academic_term = self.new_academic_term
				prog_enrollment.aghosh_home_id = self.aghosh_home_id
				prog_enrollment.student_applicant = stud.student_applicant
				prog_enrollment.school_type = stud.school_type
				prog_enrollment.building = stud.building
				prog_enrollment.room = stud.room
				prog_enrollment.bed = stud.bed
				prog_enrollment.external_school = stud.external_school
				prog_enrollment.internal_school = stud.internal_school

				prog_enrollment.student_batch_name = (
					stud.student_batch_name if stud.student_batch_name else self.new_student_batch
				)
				prog_enrollment.enrollment_date = self.enrollment_date
				prog_enrollment.save()

			elif stud.student_applicant:
				prog_enrollment = enroll_student(stud.student_applicant)
				prog_enrollment.academic_year = self.academic_year
				prog_enrollment.academic_term = self.academic_term
				prog_enrollment.aghosh_home_id = self.aghosh_home_id
				prog_enrollment.school_type = stud.school_type
				prog_enrollment.building = stud.building
				prog_enrollment.student_applicant = stud.student_applicant
				prog_enrollment.room = stud.room
				prog_enrollment.bed = stud.bed
				prog_enrollment.external_school = stud.external_school
				prog_enrollment.internal_school = stud.internal_school
				prog_enrollment.student_batch_name = (
					stud.student_batch_name if stud.student_batch_name else self.new_student_batch
				)
				prog_enrollment.save()

				#create guardian
				stud_guard=frappe.get_doc("Student Applicant", stud.student_applicant)
				create_or_update_guardian(stud_guard)
				stud_guard.save()
				if stud.school_type == "External":
					get_fee_structure_components(
						prog_enrollment,
						program = self.program,
						aghosh_home_id=self.aghosh_home_id,
						external_school=stud.external_school,
						school_type=stud.school_type
					)
				
				
				

		# frappe.msgprint(_("{0} Students have been enrolled").format(total), alert=1)

    
    
      
  
  	#Optimized Version 
	@frappe.whitelist()
	def create_sponsorships(self):
		if not self.students:
			frappe.throw(_("No students found in the Students table"))

		# total = len(self.students)
		# sponsorship_created = 0 

		# for i, student in enumerate(self.students):
			# frappe.publish_realtime(
			# 	"program_enrollment_tool", {"progress": [i + 1, total]}, user=frappe.session.user
			# )

			# # Skip student if no donors selected
			# if not student.selected_donors:
			# 	frappe.log_error(
			# 		title="Sponsorship Creation",
			# 		message="Skipping sponsorship creation due to missing donors.\nStudent: {0}".format(student.student_name or "Unknown")
			# 	)
			# 	continue  # Skip rest of this iteration entirely

			# # Now only check this if donor(s) exist
			# if not all([student.student_applicant, student.student_name]):
			# 	frappe.log_error(
			# 		title="Sponsorship Creation",
			# 		message="Skipping sponsorship creation due to missing applicant or name.\nDetails: {0}".format(frappe.as_json(student.as_dict()))
			# 	)
			# 	continue

			# # Create sponsorships for each donor
			# donor_list = student.selected_donors.split(", ")
			# print(f"This is our donor{donor_list}")
		if self.sponsors:
			for sponsor in self.sponsors:
				sponsorship = frappe.new_doc("Sponsorship")
				sponsorship.student_applicant = sponsor.student_applicant
				sponsorship.donor_id = sponsor.donor_id
				sponsorship.aghosh_home_id = self.aghosh_home_id
				sponsorship.insert(ignore_permissions=True)
				sponsorship.save()
				# sponsorship_created += 1

		# if sponsorship_created > 0:
		# 	frappe.msgprint(_("Sponsorship records created successfully"), alert=True)
		# else:
		# 	frappe.msgprint(_("No Sponsorship records were created."), alert=True)
        
    
# @frappe.whitelist()
# def get_buildings_by_aghosh_home(aghosh_home_id):
#     if not aghosh_home_id:
#         frappe.response["http_status_code"] = 400
#         return {"error": "Aghosh Home ID is required"}

#     buildings = frappe.get_all(
#         "Building",
#         filters={"aghosh_home_id": aghosh_home_id},
#         fields=["name", "type_enum"],
#         order_by="creation asc",  
#         limit_page_length=1  
#     )

#     if buildings:
#         return {"name": buildings[0]["name"]}  
#     else:
#         return {"name": None}  
    

def get_fee_structure_components(doc, program, aghosh_home_id=None, external_school=None, school_type=None):
	filters = {
		"program": program,
		"docstatus": 1
	}

	if school_type == "External" and external_school:
		filters["external_school"] = external_school
		if aghosh_home_id:
			filters["aghosh_home_id"] = aghosh_home_id
	# elif school_type == "Internal" and aghosh_home_id:
	# 	filters["aghosh_home_id"] = aghosh_home_id
	else:
		return

	fee_structure = frappe.get_value("Fee Structure", filters, "name")
	if not fee_structure:
		return

	components = frappe.get_doc("Fee Structure", fee_structure).get("components")

	for comp in components:
		doc.append("components", {
			"fees_category": comp.get("fees_category"),
			"amount": comp.get("amount"),
			"description": comp.get("description"),
			"due_date": comp.get("due_date"),
			# "discount": comp.get("discount")
		})

def create_or_update_guardian(stud): # mubarrim (under working)
	guardian_doc = frappe.get_all(
		"Guardian",
		filters={"guardian_name": stud.guardian_name},
		fields=["name"]
	)

	if guardian_doc:
		guardian = frappe.get_doc("Guardian", guardian_doc[0].name)
		guardian.guardian_name = stud.guardian_name
		guardian.guardian_gender = stud.guardian_gender
		guardian.guardian_address = stud.guardian_address
		guardian.relation_with_child = stud.relation_with_child
		guardian.guardian_occupation = stud.guardian_occupation
		guardian.guardian_qualification = stud.guardian_qualification
		guardian.guardian_marital_status = stud.guardian_marital_status
		guardian.guardian_contact_number = stud.guardian_contact_number
		guardian.guardian_cnic = stud.guardian_cnic
		guardian.save(ignore_permissions=True)
		student_id= frappe.db.get_value("Student", {"student_applicant": stud.name},"name")
		frappe.db.set_value("Student", student_id, "student_guardian_id", guardian.name)
		frappe.db.set_value("Student", student_id, "student_guardian_name", guardian.guardian_name)
		# frappe.msgprint(f"Guardian {guardian.name} updated for student {stud.student_name}")
	else:
		guardian = frappe.new_doc("Guardian")
		guardian.guardian_name = stud.guardian_name
		guardian.guardian_gender = stud.guardian_gender
		guardian.guardian_address = stud.guardian_address
		guardian.relation_with_child = stud.relation_with_child
		guardian.guardian_occupation = stud.guardian_occupation
		guardian.guardian_qualification = stud.guardian_qualification
		guardian.guardian_marital_status = stud.guardian_marital_status
		guardian.guardian_contact_number = stud.guardian_contact_number
		guardian.guardian_cnic = stud.guardian_cnic
		guardian.insert(ignore_permissions=True)
		guardian.save()
		student_id= frappe.db.get_value("Student", {"student_applicant": stud.name},"name")
		frappe.db.set_value("Student", student_id, "student_guardian_id", guardian.name)
		frappe.db.set_value("Student", student_id, "student_guardian_name", guardian.guardian_name)
		# frappe.msgprint(f"Guardian {guardian.name} created for student {stud.student_name}")