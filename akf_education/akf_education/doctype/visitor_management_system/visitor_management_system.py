import frappe
from frappe.model.document import Document

class VisitorManagementSystem(Document):
    def before_save(self):
        self.set_guardian_details()

    def set_guardian_details(self):
        if not self.cnicpassport_no:
            frappe.throw("❌ Please enter CNIC/Passport number.")

        data = frappe.db.sql("""
            SELECT 
                s.name AS student_id, 
                s.first_name
            FROM `tabStudent` s 
            INNER JOIN `tabStudent Guardian` sg ON s.name = sg.parent
            WHERE sg.guardian IN (
                SELECT name FROM `tabGuardian` WHERE cnic_number = %s
            )
        """, (self.cnicpassport_no,), as_dict=True)

        if not data:
            frappe.throw("❌ Guardian not found for this CNIC. Cannot save.")

        self.set("table", [])

        for row in data:
            self.append("table", {
                "student_id": row.student_id,
                "student_name": row.first_name
            })
