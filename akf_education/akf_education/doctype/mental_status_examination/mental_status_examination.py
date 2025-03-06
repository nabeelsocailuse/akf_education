# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MentalStatusExamination(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		additional_information: DF.SmallText | None
		amended_from: DF.Link | None
		appearance_points: DF.Literal["Clean", "Dirty", "Inappropriate", "Weird", "Others"]
		attention: DF.Literal["Suitable", "Lost", "Others"]
		behaviourattitude: DF.Literal["Collaborative", "Defensive", "Anger Issue", "More excited", "Anxious", "Terrified", "Strange and unusual"]
		concern_for_others_harm: DF.Literal["No", "There is anger", "Intended to", "There is a plan"]
		conversation: DF.Literal["Suitable", "Under Pressure", "Fast", "Weak"]
		date: DF.Date | None
		decision_making: DF.Literal["Good", "Fair", "Bad/unsuitable"]
		detachment_from_reality: DF.Literal["Not Present", "Pertaining listening", "Pertaining to seeing"]
		eye_contact: DF.Literal["Suitable", "Avoid eye contact", "Stareing", "Others"]
		facial_expressions: DF.Literal["Suitable", "Stretches on Face", "Inappropriate", "No Expressions"]
		fear_of_personal_harm: DF.Literal["Not Present", "Thinking About", "There is personal violence", "It is intended", "There is a plan"]
		impairment_in_mental_affairs_and_awareness: DF.Literal["Not Present", "Time", "Place", "Person"]
		insight: DF.Literal["Good", "Fair", "Bad/unsuitable"]
		memory_impairment: DF.Literal["Not Present", "Short Term", "Long Term", "Others"]
		mental_health_additional_info: DF.SmallText | None
		mode: DF.Literal["Suitable", "Worried", "Irritated", "In anger", "Upset", "More enthusiastic than normal children"]
		mode_additional_info: DF.SmallText | None
		name1: DF.Data | None
		obserb_additional_info: DF.SmallText | None
		physical_connection: DF.Literal["Suitable", "Disturb", "Slow", "Irrelevance"]
		staff_concerned: DF.Data | None
		unrealistic_thoughts: DF.Literal["Yes", "No", "Doubt", "A sense of superiority", "Of a religious nature"]
	# end: auto-generated types
	pass
