# # # Copyright (c) 2025, Mubarrim Iqbal and contributors
# # # For license information, please see license.txt


import frappe, ast
from frappe.model.document import Document
# from frappe.utils import getdate

class AdmissionTool(Document):
	
	@frappe.whitelist()
	def create_admissions(self):
		if(not self.admission_table): frappe.throw("First, fetch aghosh homes detail to proceed.", title="Admission Table")
		fargs = frappe._dict({
			"doctype": "Student Admission",
			"academic_year": self.academic_year,
			"admission_start_date": self.admission_start_date,
			"admission_end_date": self.admission_end_date,
			"publish_on_website": self.publish_on_website,
			"enable_admission_application": self.enable_admission_application,
			"introduction": self.introduction
		})
		for row in self.admission_table:
			fargs.update({
				"name_of_aghosh": row.aghosh_home_id,
				"title": row.aghosh_home_name,
				"route": f"admissions/{row.aghosh_home_name}",
				
			})
			if(frappe.db.exists("Student Admission", row.aghosh_home_name)):
				continue
			else:
				args = {"program_details": [{
					"program":  row.program,
					"minimum_age":  row.minimum_age,
					"maximum_age":  row.maximum_age,
				}]}
				args.update(fargs)
				doc = frappe.get_doc(args)
				doc.insert(ignore_permissions=True)
		frappe.msgprint(f"<b>{len(self.admission_table)}</b> Student admissions have been created successfully.", alert=True)

@frappe.whitelist()
def get_aghosh_homes(filters=None):
	filters = ast.literal_eval(filters) 
	conditions = get_conditions(filters)

	data = frappe.db.sql(f"""
		Select (name) as aghosh_home_id, (name1) as aghosh_home_name from `tabAghosh Home`
		Where docstatus=0
		{conditions}
	""", filters, as_dict=1)

	return data


def get_conditions(filters):
	conditions = " and region = %(region)s " if(filters.get("region")) else ""
	conditions += " and district = %(district)s " if(filters.get("district"))  else ""
	return conditions
