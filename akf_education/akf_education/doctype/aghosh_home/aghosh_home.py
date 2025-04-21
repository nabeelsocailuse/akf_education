# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AghoshHome(Document):
    def before_save(self):
        self.validate_aghosh_home()

    def validate_aghosh_home(self):
        if frappe.db.exists('Aghosh Home', {'aghosh_home_name': self.aghosh_home_name, 'name': ['!=', self.name]}):
            frappe.throw(f"Aghosh Home with name '{self.aghosh_home_name}' already exists.")
            
            
            
                        
            
@frappe.whitelist()
def get_tehsils_by_district(district):
    # Fetch the district document using district name
    district_doc = frappe.get_doc('District', district)
    
    # Initialize an empty list to store tehsils
    tehsil_list = []
    
    for row in district_doc.select_tehsil:
        tehsil_list.append({
            "tehsil_name": row.tehsil  
        })
    
    return tehsil_list


     
     
