# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class VisitorManagementSystem(Document):
    pass  # No logic here unless needed (e.g., def before_save)

@frappe.whitelist()
def guardian_details(cnic_number, parent_docname):
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

    # Ensure parent_doc exists and is not new
    if not frappe.db.exists("Visitor Management System", parent_docname):
        return "<p style='color:red;'>Document not found. Please save the form before fetching guardian data.</p>"

    parent_doc = frappe.get_doc("Visitor Management System", parent_docname)

    # Check if 'table' field exists (your child table fieldname)
    if not hasattr(parent_doc, "table"):
        return "<p style='color:red;'>Child table field 'table' not found in the parent document.</p>"

    # Clear old rows (optional – remove this if you want to append instead of replacing)
    parent_doc.set("table", [])

    for row in data:
        parent_doc.append("table", {
            "student_id": row.student_id,
            "student_name": row.first_name
        })

    parent_doc.save(ignore_permissions=True)
    return "✅ Student details have been added to the child table."
