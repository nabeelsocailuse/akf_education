# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CounslingSession(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		age: DF.Int
		dat: DF.Date | None
		date: DF.Date | None
		grade: DF.Data | None
		name1: DF.Data | None
		name2: DF.Data | None
		presenting_issues: DF.SmallText | None
		session_feedback: DF.SmallText | None
		session_goals: DF.SmallText | None
		session_number: DF.Data | None
	# end: auto-generated types
	pass
