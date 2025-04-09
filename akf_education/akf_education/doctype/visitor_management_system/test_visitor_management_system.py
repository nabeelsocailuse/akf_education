import frappe


@frappe.whitelist()
def guardian_details():
	data = frappe.db.sql("""
		SELECT 
			s.name AS student_id, 
			s.first_name
		FROM `tabStudent` s 
		INNER JOIN `tabStudent Guardian` sg 
			ON s.name = sg.parent
		WHERE sg.guardian IN (
			SELECT name 
			FROM `tabGuardian` 
			WHERE cnic_number = "2147483647"
		)
	""", as_dict=True)
	
	return data

akf_education.akf_education.doctype.visitor_management_system.test_visitor_management_system.guardian_details