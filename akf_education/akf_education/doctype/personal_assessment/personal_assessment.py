# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class PersonalAssessment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		completes_work_in_detail: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		date: DF.Date | None
		generally_trustworthy: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		gets_nervous_quickly: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		has_less_creative_hobbies: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		i_find_faults_in_others_i_disagree: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		lives_within_oneself: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		name: DF.Int | None
		outgoing_and_sociable: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		possesses_strong_ideas: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		registration_number: DF.Data
		remains_calm_deals_well_with_anxiety: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
		student_name: DF.Data | None
		tends_towards_laziness: DF.Literal["Strongly Disagree", "Somewhat Disagree", "Neutral", "Somewhat Agree", "Strongly Agree"]
	# end: auto-generated types
	pass
