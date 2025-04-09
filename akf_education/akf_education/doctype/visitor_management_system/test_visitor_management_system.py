import frappe

@frappe.whitelist()
def guardian_details(cnic_number):
	data = frappe.db.sql("""
		SELECT 
			s.name AS student_id, 
			s.first_name
		FROM `tabStudent` s 
		INNER JOIN `tabStudent Guardian` sg ON s.name = sg.parent
		WHERE sg.guardian IN (
			SELECT name FROM `tabGuardian` WHERE cnic_number = %s
		)
	""", (cnic_number,), as_dict=True)

	if not data:
		return "<p style='color:red;'>No guardian found for this CNIC.</p>"

	html = "<ul>"
	for row in data:
		html += f"<li><strong>ID:</strong> {row.student_id}, <strong>Name:</strong> {row.first_name}</li>"
	html += "</ul>"
	return html
