# import frappe

# @frappe.whitelist()
# def guardian_details(cnic_number, parent_docname):
#     data = frappe.db.sql("""
#         SELECT 
#             s.name AS student_id, 
#             s.first_name
#         FROM `tabStudent` s 
#         INNER JOIN `tabStudent Guardian` sg ON s.name = sg.parent
#         WHERE sg.guardian IN (
#             SELECT name FROM `tabGuardian` WHERE cnic_number = %s
#         )
#     """, (cnic_number,), as_dict=True)

#     if not data:
#         return "<p style='color:red;'>No guardian found for this CNIC.</p>"

#     parent_doc = frappe.get_doc("Visitor Management System", parent_docname)

#     if not hasattr(parent_doc, "table"):  
#         return "<p style='color:red;'>Child table field 'table' not found in the parent document.</p>"

#     for row in data:
#         parent_doc.append("table", {  
#             "student_id": row.student_id,
#             "student_name": row.first_name
#         })
#     parent_doc.save()

