# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentTransfer(Document):
	def before_validate(self):
		self.prefill_transfer_scenario()

	def validate(self):
		self.get_program_enrollment()
		self.prefill_transfer_scenario()

	def get_program_enrollment(self):
		if not self.student_id:
			frappe.throw("Student ID is required to proceed.")

		program_enrollment = frappe.get_all(
			"Program Enrollment",
			filters={"student": self.student_id, "docstatus": 1, "active": 1},
			fields=["aghosh_home_id", "aghosh_home_name", "building", "building_name", "room", "room_number", "bed", "bed_number"],
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
			# frappe.throw(
			# 	"Program Enrollment found: {}".format(program_enrollment)
			# )
		else:
			frappe.throw(
				"No active program enrollment found for the student with ID: {}".format(self.student_id)
			)
	
	@frappe.whitelist()
	def prefill_transfer_scenario(self):
		if self.transfer_type == "Building":
			self.new_aghosh_home_id = self.old_aghosh_home_id
			self.new_aghosh_home_name = self.old_aghosh_home_name
		
		if self.transfer_type == "Room":
			self.new_aghosh_home_id = self.old_aghosh_home_id
			self.new_aghosh_home_name = self.old_aghosh_home_name
			self.new_building_id = self.old_building_id
			self.new_building_name = self.old_building_name

		if self.transfer_type == "Bed":
			self.new_aghosh_home_id = self.old_aghosh_home_id
			self.new_aghosh_home_name = self.old_aghosh_home_name
			self.new_building_id = self.old_building_id
			self.new_building_name = self.old_building_name
			self.new_room_id = self.old_room_id
			self.new_room_number = self.old_room_number