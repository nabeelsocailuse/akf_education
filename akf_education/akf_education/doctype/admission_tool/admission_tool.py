# # # Copyright (c) 2025, Mubarrim Iqbal and contributors
# # # For license information, please see license.txt


import frappe, ast
from frappe.model.document import Document
from frappe.utils import today

class AdmissionTool(Document):
	def validate(self):
		if self.admission_start_date <= today()and self.admission_end_date < today():
			frappe.throw("Date must be today or later.")
	
	@frappe.whitelist()
	def create_admissions(self):
		if(not self.admission_table): frappe.throw("First, fetch aghosh homes detail to proceed.", title="Admission Table")
		fargs = frappe._dict({
			"doctype": "Student Admission",
			"academic_year": self.academic_year,
			"admission_start_date": self.admission_start_date,
			"admission_end_date": self.admission_end_date,
			"published": self.publish_on_website,
			"enable_admission_application": self.enable_admission_application,
			"introduction": self.introduction
		})
		for row in self.admission_table:
			if not row.program:
				frappe.throw("Program is missing for Aghosh Home.")
			if not row.minimum_age or not row.maximum_age:
				frappe.throw ("Age limit missing")
    
			fargs.update({
				"aghosh_home_id": row.aghosh_home_id,
				"title": f"{row.aghosh_home_name} - ({self.academic_year}) - {row.program}",
				"route": f"admissions/{row.aghosh_home_name}/{self.academic_year}/{row.program}",
				
			})
			if(frappe.db.exists("Student Admission", {"aghosh_home_name": row.aghosh_home_name, "academic_year": self.academic_year, "program": row.program})):
				frappe.throw(f"Already an admission exist against {row.aghosh_home_name}, {row.academic_year} and {row.program}", title="Duplicate Admission Entry")
				continue
			else:
				args = {"program_details": [{
					"program":  row.program,
					"min_age":  row.minimum_age,
					"max_age":  row.maximum_age,
				}]}
				args.update(fargs)
				doc = frappe.get_doc(args)
				# frappe.throw(f"{doc}")
				doc.insert(ignore_permissions=True)
		frappe.msgprint(f"<b>{len(self.admission_table)}</b> Student admissions have been created successfully.", alert=True)

@frappe.whitelist()
def get_aghosh_homes(filters=None):
	filters = ast.literal_eval(filters) 
	conditions = get_conditions(filters)

	data = frappe.db.sql(f"""
		Select (name) as aghosh_home_id, (aghosh_home_name) as aghosh_home_name from `tabAghosh Home`
		Where docstatus=0
		{conditions}
	""", filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = " and region = %(region)s " if(filters.get("region")) else ""
	conditions += " and district = %(district)s " if(filters.get("district"))  else ""
	return conditions
