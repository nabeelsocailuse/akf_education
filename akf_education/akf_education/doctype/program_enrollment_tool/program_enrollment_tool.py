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
		academic_term_reqd = cint(
			frappe.db.get_single_value("Education Settings", "academic_term_reqd")
		)
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
		
		# self.creating_orphan()
 

	def enrolled_students(self):
		total = len(self.students)
		for i, stud in enumerate(self.students):
			frappe.publish_realtime(
				"program_enrollment_tool", dict(progress=[i + 1, total]), user=frappe.session.user
			)
			if stud.student:
				prog_enrollment = frappe.new_doc("Program Enrollment")
				prog_enrollment.student = stud.student
				prog_enrollment.student_name = stud.student_name
				prog_enrollment.student_category = stud.student_category
				prog_enrollment.program = self.new_program
				prog_enrollment.academic_year = self.new_academic_year
				prog_enrollment.academic_term = self.new_academic_term
				prog_enrollment.aghosh_home = self.aghosh_home1
				prog_enrollment.school_type = stud.school_type1
				prog_enrollment.building = stud.building
				prog_enrollment.room = stud.room
				prog_enrollment.bed = stud.bed
				prog_enrollment.external1 = stud.external

				prog_enrollment.student_batch_name = (
					stud.student_batch_name if stud.student_batch_name else self.new_student_batch
				)
				prog_enrollment.enrollment_date = self.enrollment_date
				prog_enrollment.save()

			elif stud.student_applicant:
				prog_enrollment = enroll_student(stud.student_applicant)
				prog_enrollment.academic_year = self.academic_year
				prog_enrollment.academic_term = self.academic_term
				prog_enrollment.aghosh_home = self.aghosh_home1
				prog_enrollment.school_type = stud.school_type1
				prog_enrollment.building = stud.building
				prog_enrollment.room = stud.room
				prog_enrollment.bed = stud.bed
				prog_enrollment.external1 = stud.external
				prog_enrollment.student_batch_name = (
					stud.student_batch_name if stud.student_batch_name else self.new_student_batch
				)
				prog_enrollment.save()
				

		frappe.msgprint(_("{0} Students have been enrolled").format(total), alert=1)
  
  
  
  
  
	
	# def creating_orphan(self):
	# 	total = len(self.students)
	# 	# frappe.msgprint(_("Total Students: {0}").format(total))

	# 	for i, stud in enumerate(self.students):
	# 		try:
	# 			frappe.publish_realtime(
	# 				"program_enrollment_tool", {"progress": [i + 1, total]}, user=frappe.session.user
	# 			)

	# 			# frappe.msgprint(_("Processing student {0}/{1}").format(i + 1, total))

	# 			if not stud.student_name:  
	# 				# frappe.msgprint(_("Skipping student {0} - No valid student name").format(i + 1))
	# 				continue

	# 			# frappe.msgprint(_("Creating orphan record for student: {0}").format(stud.student_name))

	# 			orphan = frappe.new_doc("Orphan")
	# 			orphan.child_name = stud.student_name 
	# 			orphan.current_aghosh_id = self.aghosh_home1 
	# 			orphan.save()

	# 			frappe.msgprint(_("Orphan record created successfully for {0}.").format(stud.student_name), alert=1)

	# 		except Exception as e:
	# 			frappe.log_error(frappe.get_traceback(), "Creating Orphan Error")
	# 			# frappe.msgprint(_("An error occurred: {0}").format(str(e)))
    
    
    
    

	# @frappe.whitelist()
	# def create_sponsorships(self):
	# 	students = frappe.get_all(
	# 		"Program Enrollment Tool Student",
	# 		fields=["student_applicant", "student_name", "selected_donors"]
	# 	)

	# 	total = len(students)

	# 	if not students:
	# 		frappe.throw(_("No students found in Program Enrollment Tool Student"))

	# 	for i, student in enumerate(students):
	# 		frappe.publish_realtime(
	# 			"program_enrollment_tool", {"progress": [i + 1, total]}, user=frappe.session.user
	# 		)

	# 		student_applicant = student.get("student_applicant")
	# 		student_name = student.get("student_name")
	# 		selected_donors = student.get("selected_donors")

	# 		if not student_applicant or not student_name or not selected_donors:
	# 			frappe.log_error(f"Skipping record due to missing data: {student}", "Sponsorship Creation")
	# 			continue

	# 		donors = selected_donors.split(", ")

	# 		for donor in donors:
	# 			sponsorship = frappe.new_doc("Sponsorship")
	# 			sponsorship.student_applicant = student_applicant
	# 			sponsorship.aghosh_home = self.aghosh_home1
	# 			sponsorship.donor_id = donor
	# 			sponsorship.save()

	# 	frappe.msgprint(_("Sponsorship records created successfully").format(total), alert=1)
  
  
  #Optimized Version 
	@frappe.whitelist()
	def create_sponsorships(self):
		if not self.students:
			frappe.throw(_("No students found in the Students table"))

		total = len(self.students)

		for i, student in enumerate(self.students):
			frappe.publish_realtime(
				"program_enrollment_tool", {"progress": [i + 1, total]}, user=frappe.session.user
			)

			if not all([student.student_applicant, student.student_name, student.selected_donors]):
				frappe.log_error(f"Skipping record due to missing data: {student.as_dict()}", "Sponsorship Creation")
				continue

			donor_list = student.selected_donors.split(", ")

			for donor in donor_list:
				sponsorship = frappe.new_doc("Sponsorship")
				sponsorship.student_applicant = student.student_applicant
				sponsorship.aghosh_home = self.aghosh_home1
				sponsorship.donor_id = donor
				sponsorship.insert(ignore_permissions=True)
				
		frappe.msgprint(_("Sponsorship records created successfully"), alert=True)



        
    
@frappe.whitelist()
def get_buildings_by_aghosh_home(aghosh_home1):
    if not aghosh_home1:
        frappe.response["http_status_code"] = 400
        return {"error": "Aghosh Home ID is required"}

    buildings = frappe.get_all(
        "Building",
        filters={"aghosh_home_id": aghosh_home1},
        fields=["name", "type_enum"],
        order_by="creation asc",  
        limit_page_length=1  
    )

    if buildings:
        return {"name": buildings[0]["name"]}  
    else:
        return {"name": None}  
    
    



# @frappe.whitelist()
# def get_donors(donor_id=None):
#     filters = {"docstatus": ["!=", 2]}

#     if donor_id:  # Apply filter if donor_id is provided
#         filters["name"] = ["like", f"%{donor_id}%"]

#     donors = frappe.get_all("Donor", filters=filters, fields=["name"])
#     return donors    


# @frappe.whitelist()
# def create_sponsorships(donors, student_applicant):
#     donors = json.loads(donors)  # Convert JSON string to Python list if needed

#     if not donors or not student_applicant:
#         frappe.throw(_("Please select a donor and ensure student details are available."))

#     for donor in donors:
#         sponsorship = frappe.new_doc("Sponsorship")
#         sponsorship.student_applicant = student_applicant  # Associate with selected student
#         sponsorship.donor_id = donor.get("name")  # Assuming 'name' contains donor ID
#         # sponsorship.sponsorship_date = frappe.utils.today()
#         sponsorship.save()

#     return "Sponsorships created successfully!!!"










# @frappe.whitelist()
# def create_sponsorships(donors, student_applicant):
#     donors = json.loads(donors)  # Convert JSON string to Python list if needed

#     if not donors or not student_applicant:
#         frappe.throw(_("Please select a donor and ensure student details are available."))

#     for donor in donors:
#         sponsorship = frappe.new_doc("Sponsorship")
#         sponsorship.student_applicant = student_applicant  # Associate with selected student
#         sponsorship.donor = donor.get("name")  # Assuming 'name' contains donor ID
#         sponsorship.sponsorship_date = frappe.utils.today()
#         sponsorship.save()

#     return "Sponsorships created successfully!"







	
 
 
 















					



 
    
    
    
    
    
    
    

    
 
    
    
    
    
    
    

    
    
    
    
    


    
    
    









		
		
  
		
  
  
  
  	

  


				
		
		
		


    

		
     
