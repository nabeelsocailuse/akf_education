import frappe
from frappe.model.document import Document

class VisitorManagementSystem(Document):
    def validate(self):
        if self.purpose_of_visit == "Meeting Resident" and self.cnicpassport_no:
            fetch_guardian_student_details(self)

@frappe.whitelist()
def guardian_details(cnic_number, parent_docname):
    doc = frappe.get_doc("Visitor Management System", parent_docname)
    return fetch_guardian_student_details(doc)

def fetch_guardian_student_details(doc):
    doc.set("table", [])

    guardian = frappe.db.get_value("Guardian", {"guardian_cnic": doc.cnicpassport_no}, "name")
    if not guardian:
        frappe.throw("❌ Guardian not found for this CNIC")
    # frappe.throw(f"Guardian: {guardian}")

    data = frappe.db.sql("""
    SELECT name, full_name
    FROM `tabStudent`
    WHERE student_guardian_id = %s
""", (guardian,), as_dict=True)
    # frappe.throw(f"Data: {data}")

    if not data:
        frappe.throw("❌ Student not available against this guardian.")
        
    for row in data:
        doc.append("table", {
            "student_id": row.name,
            "student_name": row.full_name
        })
