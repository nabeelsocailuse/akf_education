# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Building(Document):
	def autoname(self):
		self.name = make_autoname(f"AA-B-{self.aghosh_region_code}-.###")
