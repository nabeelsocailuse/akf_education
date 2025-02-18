# Copyright (c) 2025, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class careercounsellingchild(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		obtained_mark: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percentage: DF.Data | None
		subjects: DF.Data | None
		total_marksout_of: DF.Data | None
	# end: auto-generated types
	pass
