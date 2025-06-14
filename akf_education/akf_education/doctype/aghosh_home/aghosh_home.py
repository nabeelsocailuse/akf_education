# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class AghoshHome(Document):
    def before_save(self):
        self.validate_aghosh_home()

    def validate_aghosh_home(self):
        if frappe.db.exists('Aghosh Home', {'aghosh_home_name': self.aghosh_home_name, 'name': ['!=', self.name]}):
            frappe.throw(f"Aghosh Home with name '{self.aghosh_home_name}' already exists.")

    def autoname(self):
        self.name = make_autoname(f"AA-{self.region_code}-.####")
            
# @frappe.whitelist()
# def get_region_and_tehsil(region=None, district=None):
#     result = {}

#     if region:
#         region_doc = frappe.get_doc('Region', region)
#         district_list = []
#         for row in region_doc.table:
#             district_list.append({
#                 "district_name": row.district
#             })
#         result["districts"] = district_list

#     if district:
#         district_doc = frappe.get_doc('District', district)
#         tehsil_list = []
#         for row in district_doc.select_tehsil:
#             tehsil_list.append({
#                 "tehsil_name": row.tehsil
#             })
#         result["tehsils"] = tehsil_list

#     return result

