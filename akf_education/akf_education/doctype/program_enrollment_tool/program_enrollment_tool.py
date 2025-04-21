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
		elif not self.program:
			frappe.throw ("Select Program")
		elif not self.aghosh_home1:
			frappe.throw ("Select Aghosh Home")
   
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
					.where(student_applicant.aghosh_home == self.aghosh_home1)
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
			if not stud.bed:
				frappe.throw("please select bed for the student first")
			if not stud.school_type1:
				frappe.throw("Please select student type.")
			# if not stud.selected_donors:
			# 	frappe.throw("Select Donor and Press Save Button First")
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
  
  
  
  
  
  	#Optimized Version 
	@frappe.whitelist()
	def create_sponsorships(self):
		if not self.students:
			frappe.throw(_("No students found in the Students table"))

		total = len(self.students)
		sponsorship_created = 0 

		for i, student in enumerate(self.students):
			frappe.publish_realtime(
				"program_enrollment_tool", {"progress": [i + 1, total]}, user=frappe.session.user
			)

			# Skip student if no donors selected
			if not student.selected_donors:
				frappe.log_error(
					title="Sponsorship Creation",
					message="Skipping sponsorship creation due to missing donors.\nStudent: {0}".format(student.student_name or "Unknown")
				)
				continue  # Skip rest of this iteration entirely

			# Now only check this if donor(s) exist
			if not all([student.student_applicant, student.student_name]):
				frappe.log_error(
					title="Sponsorship Creation",
					message="Skipping sponsorship creation due to missing applicant or name.\nDetails: {0}".format(frappe.as_json(student.as_dict()))
				)
				continue

			# Create sponsorships for each donor
			donor_list = student.selected_donors.split(", ")
			for donor in donor_list:
				sponsorship = frappe.new_doc("Sponsorship")
				sponsorship.student_applicant = student.student_applicant
				sponsorship.aghosh_home = self.aghosh_home1
				sponsorship.donor_id = donor
				sponsorship.insert(ignore_permissions=True)
				sponsorship.save()
				sponsorship_created += 1

		if sponsorship_created > 0:
			frappe.msgprint(_("Sponsorship records created successfully"), alert=True)
		else:
			frappe.msgprint(_("No Sponsorship records were created."), alert=True)




        
    
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







	
 
 
 















					



 
    
    
    
    
    
    
    

    
 
    
    
    
    
    
    

    
    
    
    
    


    
    
    









		
		
  
		
  
  
  
  	

  


				
		
		
		


    

		
     
