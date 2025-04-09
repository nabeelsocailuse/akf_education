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

	# Start building styled HTML
	html = """
		<div style="margin-top: 10px;">
			<h4>Student Details</h4>
			<div style="border: 1px solid #ccc; border-radius: 6px; padding: 10px;">
	"""

	for row in data:
		html += f"""
			<div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
				<div><strong>Student ID:</strong> {row.student_id}</div>
				<div><strong>Name:</strong> {row.first_name}</div>
			</div>
		"""

	html += "</div></div>"
	return html
