# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PastandPresentInformation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		age: DF.Int
		alive: DF.Literal["Yes", "No"]
		birth_number_among_siblings: DF.Data | None
		date: DF.Date
		date_of_birt: DF.Date | None
		date_of_birth: DF.Date | None
		date_of_death: DF.Date | None
		early_development: DF.SmallText | None
		early_exposure_to_drugs_if_any: DF.SmallText | None
		economic_status: DF.Data | None
		educational_status: DF.Data | None
		family_type: DF.Literal["individual", "Joint Family"]
		father_name: DF.Data | None
		fathers_occupation: DF.Data | None
		gender: DF.Data | None
		language_and_speech_history: DF.SmallText | None
		medicalphysical_illnesses_and_history: DF.SmallText | None
		mother_name: DF.Data | None
		number_of_siblings: DF.Data | None
		physical_and_hereditary_diseases_in_the_family: DF.SmallText | None
		psychological_or_mental_illnesses_in_the_family: DF.SmallText | None
		psychological_problems: DF.SmallText | None
		psychologists_opinion: DF.SmallText | None
		reason_of_death: DF.Data | None
		registration_number: DF.Data
		second_marriage: DF.Data | None
		student_name: DF.Data | None
		tentative_diagnosis: DF.SmallText | None
		traumatic_experiences: DF.SmallText | None
	# end: auto-generated types
	pass
