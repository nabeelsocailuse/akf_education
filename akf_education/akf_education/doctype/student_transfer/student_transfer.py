# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentTransfer(Document):
	# def before_validate(self):
	# 	self.prefill_transfer_scenario()

	def validate(self):
		self.get_program_enrollment()
		# self.prefill_transfer_scenario()
	
	def on_submit(self):
		if not self.new_building_id or  not self.new_room_id or not self.new_bed_id:
			frappe.throw("Building, Room, and Bed information is required for transfer.")
			
		self.create_program_enrollment()

	@frappe.whitelist()
	def get_program_enrollment(self):
		if not self.student_id:
			frappe.throw("Student ID is required to proceed.")

		program_enrollment = frappe.get_all(
			"Program Enrollment",
			filters={"student": self.student_id, "docstatus": 1, "active": 1},
			fields=["aghosh_home_id", "aghosh_home_name", "building", "building_name", "room", "room_number", "bed", "bed_number", "program", "academic_year"],
			order_by="creation desc",
			limit=1,
		)

		if program_enrollment:
			self.old_aghosh_home_id = program_enrollment[0].aghosh_home_id
			self.old_aghosh_home_name = program_enrollment[0].aghosh_home_name
			self.old_building_id = program_enrollment[0].building
			self.old_building_name = program_enrollment[0].building_name
			self.old_room_id = program_enrollment[0].room
			self.old_room_number = program_enrollment[0].room_number
			self.old_bed_id = program_enrollment[0].bed
			self.old_bed_number = program_enrollment[0].bed_number
			self.program = program_enrollment[0].program
			self.academic_year = program_enrollment[0].academic_year
			# frappe.throw(
			# 	"Program Enrollment found: {}".format(program_enrollment)
			# )
		else:
			frappe.throw(
				"No active program enrollment found for the student with ID: {}".format(self.student_id)
			)
	
	@frappe.whitelist()
	def prefill_transfer_scenario(self):
		if self.transfer_type == "Aghosh Home":
			self.new_aghosh_home_id = ''
			self.new_aghosh_home_name = ''
			self.new_building_id = ''
			self.new_building_name = ''
			self.new_room_id = ''
			self.new_room_number = ''
			self.new_bed_id = ''
			self.new_bed_number = ''
			self.school_type = ''
			self.internal_school = ''
			self.internal_school_name = ''
			self.external_school = ''
			self.external_school_name = ''

		if self.transfer_type == "Building":
			self.new_aghosh_home_id = self.old_aghosh_home_id
			self.new_aghosh_home_name = self.old_aghosh_home_name
			self.new_building_id = ''
			self.new_building_name = ''
			self.new_room_id = ''
			self.new_room_number = ''
			self.new_bed_id = ''
			self.new_bed_number = ''
		
		if self.transfer_type == "Room":
			self.new_aghosh_home_id = self.old_aghosh_home_id
			self.new_aghosh_home_name = self.old_aghosh_home_name
			self.new_building_id = self.old_building_id
			self.new_building_name = self.old_building_name
			self.new_room_id = ''
			self.new_room_number = ''
			self.new_bed_id = ''
			self.new_bed_number = ''

		if self.transfer_type == "Bed":
			self.new_aghosh_home_id = self.old_aghosh_home_id
			self.new_aghosh_home_name = self.old_aghosh_home_name
			self.new_building_id = self.old_building_id
			self.new_building_name = self.old_building_name
			self.new_room_id = self.old_room_id
			self.new_room_number = self.old_room_number
			self.new_bed_id = ''
			self.new_bed_number = ''

	def create_program_enrollment(self):
		# if not self.student_id:
		# 	frappe.throw("Student ID is required to create a new program enrollment.")

		program_enrollment = frappe.new_doc("Program Enrollment")
		program_enrollment.student = self.student_id
		program_enrollment.aghosh_home_id = self.new_aghosh_home_id
		program_enrollment.aghosh_home_name = self.new_aghosh_home_name
		program_enrollment.building = self.new_building_id
		program_enrollment.building_name = self.new_building_name
		program_enrollment.room = self.new_room_id
		program_enrollment.room_number = self.new_room_number
		program_enrollment.bed = self.new_bed_id
		program_enrollment.bed_number = self.new_bed_number
		program_enrollment.school_type = self.school_type
		program_enrollment.internal_school = self.internal_school
		program_enrollment.internal_school_name = self.internal_school_name
		program_enrollment.external_school = self.external_school
		program_enrollment.external_school_name = self.external_school_name
		program_enrollment.program = self.program
		program_enrollment.academic_year = self.academic_year
		# program_enrollment.active = 1  # Set the new enrollment as active
		self.program_enrollment = program_enrollment.name  # Store the name of the new program enrollment
		program_enrollment.student_transfer = self.name  # Link the program enrollment to this transfer document

		program_enrollment.insert()
		frappe.msgprint("New Program Enrollment created successfully for Student ID: {}".format(self.student_id))