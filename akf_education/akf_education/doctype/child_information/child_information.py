# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ChildInformation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		age: DF.Data | None
		aghosh: DF.Data | None
		any_murmur: DF.Data | None
		bpmm_of_hg: DF.Data | None
		child_id: DF.Data | None
		clothing: DF.Literal["Cleaned:1", "Dirty:0"]
		clubbing: DF.Data | None
		cyanosis: DF.Data | None
		dental_hygiene: DF.Literal["Good", "Satisfactory", "Poor"]
		ears: DF.Literal["Pinna/Clean:1", "Pinna/Dirty:0", "wax:1", "WAX:0"]
		ears_ltnab: DF.Data | None
		ears_rtnab: DF.Data | None
		eye_ltnab: DF.Data | None
		eye_rtnab: DF.Data | None
		eyes: DF.Literal["Clean:1", "Dirty:0"]
		father_name: DF.Data | None
		gait: DF.Data | None
		gender: DF.Literal["Male", "Female"]
		general_physical_apperance: DF.SmallText | None
		gumsnab: DF.Data | None
		hair: DF.Literal["Cleaned/Combed:1", "Not Cleaned/Combed:0"]
		handsnailsnab: DF.Data | None
		height: DF.Data | None
		hygiene_score2: DF.Data | None
		hygiene_score: DF.Data | None
		jaundice2: DF.Data | None
		jaundice: DF.Data | None
		mother_name: DF.Data | None
		nail: DF.Literal["Cleaned/cut:1", "Not Cleaned/cut:0"]
		name1: DF.Data | None
		nose2: DF.Data | None
		nose: DF.Data | None
		nutrition_status: DF.Literal["Good", "Satisfactory", "Poor"]
		posture: DF.Data | None
		pulsemin: DF.Data | None
		resp_rate: DF.Data | None
		skin: DF.Literal["Healthy/shinning:1", "Unhealthy:0"]
		teethnab: DF.Data | None
		tempf: DF.Data | None
		throatnab: DF.Data | None
		tonguenab: DF.Data | None
		weight_now: DF.Data | None
	# end: auto-generated types
	pass
