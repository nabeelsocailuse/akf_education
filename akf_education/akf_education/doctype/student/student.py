# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
import re
from frappe import _
from datetime import date
from frappe.desk.form.linked_with import get_linked_doctypes
from frappe.model.document import Document
from frappe.utils import getdate, today
from erpnext import get_default_currency
from frappe.utils.nestedset import get_root_of
from frappe.utils import validate_email_address
from datetime import datetime, date

# from akf_education.akf_education.workspace.aghosh.utils import check_content_completion, check_quiz_completion
from education.education.utils import check_content_completion, check_quiz_completion




class Student(Document):
	def validate(self):
		self.set_title()
		self.validate_dates()
		self.validate_user()
		# if self.student_applicant:
		# 	self.set_guardians_from_applicant()
   
		if self.date_of_birth:
			self.age = self.calculate_age()
   		
		if self.student_applicant:
			self.check_unique()
			self.update_applicant_status()
   
	# def on_trash(self):
	# 	self.delete_guardian()
   
               	 	
	# def on_update(self):
	# 	# for each student check whether a customer exists or not if it does not exist then create a customer with customer group student
	# 	# This prevents from polluting users data
	# 	self.set_missing_customer_details()
  
	# def calculate_age(self):
	# 	dob = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
	# 	# dob = self.date_of_birth
	# 	today = date.today()
	# 	return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
	def calculate_age(self):
		from frappe.utils import nowdate
		from datetime import datetime
		
		today = datetime.strptime(nowdate(), "%Y-%m-%d")
		date_obj =frappe.utils.getdate(self.date_of_birth)
		date_str = date_obj.strftime('%Y-%m-%d')
		birth_date = datetime.strptime(date_str, "%Y-%m-%d")
		
		age = today.year - birth_date.year
		if (today.month, today.day) < (birth_date.month, birth_date.day):
			age -= 1
		return age

	def delete_guardian(self):
		if self.student_applicant:
			guardians = frappe.get_all(
				"Guardian",
				filters={"student_applicant": self.student_applicant},
				pluck="name"
			)
			for guardian in guardians:
				frappe.delete_doc("Guardian", guardian, force=1)
				frappe.msgprint(
					f"Guardian {guardian} deleted for Student Applicant {self.student_applicant}",
					alert=True
				)

	def set_guardians_from_applicant(self):
		if not self.student_applicant:
			return

		guardians = frappe.get_all(
			"Guardian",
			filters={"student_applicant": self.student_applicant},
			fields=["name", "guardian_name", "relation_with_child", "mobile_number"]
		)
		frappe.msgprint(f"Guardians fetched: {frappe.as_json(guardians)}")
		if not guardians:
			frappe.msgprint("No guardians found for this applicant", alert=True)
			return

		# Clear existing guardians
		self.guardians = []

		for g in guardians:
			self.append("guardians", {
				"guardian": g.name,
				"guardian_name": g.guardian_name or "",
				"relation_with_child": g.relation_with_child or "",
				"mobile_number": g.mobile_number or ""
			})	
		

	def set_missing_customer_details(self):
		self.set_customer_group()
		if self.customer:
			self.update_linked_customer()
		else:
			self.create_customer()

	def set_customer_group(self):
		if not self.customer_group:
			self.customer_group = "Student"
			frappe.db.set_value("Student", self.name, "customer_group", "Student")

	# Validate Functions
	def set_title(self):
		self.full_name = " ".join(
			filter(None, [self.first_name, self.middle_name, self.last_name])
		)

	def validate_dates(self):
		for sibling in self.siblings:
			if sibling.date_of_birth and getdate(sibling.date_of_birth) > getdate():
				frappe.throw(
					_("Row {0}:Sibling Date of Birth cannot be greater than today.").format(
						sibling.idx
					)
				)

		if self.date_of_birth and getdate(self.date_of_birth) >= getdate():
			frappe.throw(_("Date of Birth cannot be greater than today."))

		if self.date_of_birth and getdate(self.date_of_birth) >= getdate(self.joining_date):
			frappe.throw(_("Date of Birth cannot be greater than Joining Date."))

		if (
			self.joining_date
			and self.date_of_leaving
			and getdate(self.joining_date) > getdate(self.date_of_leaving)
		):
			frappe.throw(_("Joining Date can not be greater than Leaving Date"))
   


	# def validate_user(self):
	# 	"""Create a website user for student creation if not already exists"""
	# 	if not frappe.db.get_single_value(
	# 		"Education Settings", "user_creation_skip"
	# 	) and not frappe.db.exists("User", self.student_email_id):
	# 		student_user = frappe.get_doc(
	# 			{
	# 				"doctype": "User",
	# 				"first_name": self.first_name,
	# 				"last_name": self.last_name,
	# 				# "email": self.student_email_id,
	# 				"gender": self.gender,
	# 				# "send_welcome_email": 1,
	# 				"user_type": "Website User",
	# 			}
	# 		)
	# 		student_user.add_roles("Student")
	# 		student_user.save(ignore_permissions=True)

	# 		self.user = student_user.name
 
	def validate_user(self):
		"""Create a website user for student creation if not already exists"""
		email = self.student_email_id

		if not frappe.db.get_single_value("Education Settings", "user_creation_skip"):

			# Only proceed if email is present and valid
			if email:
				try:
					validate_email_address(email, throw=True)
				except frappe.exceptions.InvalidEmailAddressError:
					frappe.throw(f"'{email}' is not a valid Email Address")

				if not frappe.db.exists("User", email):
					student_user = frappe.get_doc({
						"doctype": "User",
						"email": email,
						"first_name": self.first_name,
						"last_name": self.last_name,
						"gender": self.gender,
						"user_type": "Website User",
					})
					student_user.add_roles("Student")
					student_user.save(ignore_permissions=True)
					self.user = student_user.name
			else:
				pass
				# frappe.msgprint("Student Email ID is not provided. User not created.") 

	def check_unique(self):
		"""Validates if the Student Applicant is Unique"""
		student = frappe.get_all(
			"Student",
			{"student_applicant": self.student_applicant, "name": ["!=", self.name]},
			pluck="name",
		)
		if len(student):
			frappe.throw(
				_("Student {0} exist against student applicant {1}").format(
					student[0], self.student_applicant
				)
			)

	def update_applicant_status(self):
		"""Updates Student Applicant status to Enrolled"""
		if self.student_applicant:
			frappe.db.set_value(
				"Student Applicant", self.student_applicant, "application_status", "Enrolled"
			)

	# End of Validate Functions

	# On Update Functions
	def update_linked_customer(self):
		customer = frappe.get_doc("Customer", self.customer)
		if self.customer_group:
			customer.customer_group = self.customer_group
		customer.customer_name = self.student_name
		customer.image = self.image
		customer.save()

		frappe.msgprint(_("Customer {0} updated").format(customer.name), alert=True)

	def create_customer(self):
		customer = frappe.get_doc(
			{
				"doctype": "Customer",
				"customer_name": self.student_name,
				"customer_group": self.customer_group
				or frappe.db.get_single_value("Selling Settings", "customer_group"),
				"customer_type": "Individual",
				"image": self.image,
			}
		).insert()

		frappe.db.set_value("Student", self.name, "customer", customer.name)
		frappe.msgprint(
			_("Customer {0} created and linked to Student").format(customer.name), alert=True
		)

	def get_all_course_enrollments(self):
		"""Returns a list of course enrollments linked with the current student"""
		course_enrollments = frappe.get_all(
			"Course Enrollment", filters={"student": self.name}, fields=["course", "name"]
		)
		if not course_enrollments:
			return None
		else:
			enrollments = {item["course"]: item["name"] for item in course_enrollments}
			return enrollments

	def get_program_enrollments(self):
		"""Returns a list of course enrollments linked with the current student"""
		program_enrollments = frappe.get_all(
			"Program Enrollment", filters={"student": self.name}, fields=["program"]
		)
		if not program_enrollments:
			return None
		else:
			enrollments = [item["program"] for item in program_enrollments]
			return enrollments

	def get_topic_progress(self, course_enrollment_name, topic):
		"""
		Get Progress Dictionary of a student for a particular topic
		        :param self: Student Object
		        :param course_enrollment_name: Name of the Course Enrollment
		        :param topic: Topic DocType Object
		"""
		contents = topic.get_contents()
		progress = []
		if contents:
			for content in contents:
				if content.doctype in ("Article", "Video"):
					status = check_content_completion(
						content.name, content.doctype, course_enrollment_name
					)
					progress.append(
						{"content": content.name, "content_type": content.doctype, "is_complete": status}
					)
				elif content.doctype == "Quiz":
					status, score, result, time_taken = check_quiz_completion(
						content, course_enrollment_name
					)
					progress.append(
						{
							"content": content.name,
							"content_type": content.doctype,
							"is_complete": status,
							"score": score,
							"result": result,
						}
					)
		return progress

	def enroll_in_program(self, program_name):
		try:
			enrollment = frappe.get_doc(
				{
					"doctype": "Program Enrollment",
					"student": self.name,
					"academic_year": frappe.get_last_doc("Academic Year").name,
					"program": program_name,
					"enrollment_date": frappe.utils.datetime.datetime.now(),
				}
			)
			enrollment.save(ignore_permissions=True)
		except frappe.exceptions.ValidationError:
			enrollment_name = frappe.get_list(
				"Program Enrollment", filters={"student": self.name, "Program": program_name}
			)[0].name
			return frappe.get_doc("Program Enrollment", enrollment_name)
		else:
			enrollment.submit()
			return enrollment

	def enroll_in_course(self, course_name, program_enrollment, enrollment_date=None):
		if enrollment_date is None:
			enrollment_date = frappe.utils.datetime.datetime.now()
		try:
			enrollment = frappe.get_doc(
				{
					"doctype": "Course Enrollment",
					"student": self.name,
					"course": course_name,
					"program_enrollment": program_enrollment,
					"enrollment_date": enrollment_date,
				}
			)
			enrollment.save(ignore_permissions=True)
		except frappe.exceptions.ValidationError:
			enrollment_name = frappe.get_list(
				"Course Enrollment",
				filters={
					"student": self.name,
					"course": course_name,
					"program_enrollment": program_enrollment,
				},
			)[0].name
			return frappe.get_doc("Course Enrollment", enrollment_name)
		else:
			return enrollment




def get_timeline_data(doctype, name):
	"""Return timeline for attendance"""
	return dict(
		frappe.db.sql(
			"""select unix_timestamp(`date`), count(*)
		from `tabStudent Attendance` where
			student=%s
			and `date` > date_sub(curdate(), interval 1 year)
			and docstatus = 1 and status = 'Present'
			group by date""",
			name,
		)
	)
 




		
    


    









