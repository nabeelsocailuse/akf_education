# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CareerCounsellingForm(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.custom_module.doctype.brothers_and_sisters.brothers_and_sisters import BrothersandSisters
		from frappe.custom_module.doctype.career_counselling_child.career_counselling_child import careercounsellingchild
		from frappe.types import DF

		accountant_______ccaccaacma: DF.Check
		aghosh_address: DF.Data | None
		agricultural_medicine: DF.Check
		aim_of_life: DF.SmallText | None
		anatomy: DF.Check
		architect: DF.Check
		biotechnology: DF.Check
		birth_order: DF.Data | None
		birth_place: DF.Data | None
		business_administration: DF.Check
		careers_goal_what_i_want_to_become: DF.SmallText | None
		cause_of_death: DF.Data | None
		chemistry: DF.Check
		current_class: DF.Data | None
		cyber_security: DF.Check
		date: DF.Date | None
		date_of_death: DF.Date | None
		designing_degree: DF.Check
		district: DF.Data | None
		doctor_medical_filed: DF.Check
		economist: DF.Check
		engineering: DF.Check
		family_system: DF.Literal["Nuclear", "Joint"]
		father_name: DF.Data | None
		father_occupation: DF.Data | None
		gender: DF.Literal["Male", "Female"]
		genetics: DF.Check
		geography: DF.Check
		govt_job: DF.Check
		guardian_name: DF.Data | None
		guardian_occupation: DF.Data | None
		hobbies: DF.SmallText | None
		industrial_and_manufacturing: DF.Check
		it_professional: DF.Check
		join_pak_army: DF.Check
		lawyer: DF.Check
		marital_status_of_mother: DF.Literal["Married", "Separated", "Divorced", "Widowed"]
		mass_communication: DF.Check
		mathematics: DF.Check
		microbiology: DF.Check
		mother_name: DF.Data | None
		mother_occupation: DF.Data | None
		name1: DF.Data | None
		name: DF.Int | None
		number_of_sibling: DF.Data | None
		obtained_marks__total_mark: DF.Data | None
		obtained_marks__total_marks: DF.Data | None
		others: DF.Check
		percentag: DF.Data | None
		percentage: DF.Data | None
		pervious_class: DF.Data | None
		pharmacy: DF.Check
		physics: DF.Check
		pilots: DF.Check
		police: DF.Check
		political_science: DF.Check
		province: DF.Data | None
		psychology: DF.Check
		relationship: DF.Data | None
		social_worker: DF.Check
		table_lmwv: DF.Table[BrothersandSisters]
		table_mrfp: DF.Table[careercounsellingchild]
		table_wrka: DF.Table[careercounsellingchild]
		table_ykje: DF.Table[careercounsellingchild]
		teachingprofessor: DF.Check
		tehsil: DF.Data | None
		village__city: DF.Data | None
	# end: auto-generated types
	pass
