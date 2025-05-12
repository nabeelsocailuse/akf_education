
import frappe
from frappe import _


def get_context(context):
    # frappe.throw(f"{context}")
	# do your magic here
	pass




# @frappe.whitelist()
# def get_student_admission_program_details(academic_year, program):
#     result = frappe.db.sql("""
#         SELECT
#             sa.name AS admission_name,
#             sa.academic_year,
#             sa.aghosh_home_id,
#             sa.aghosh_home_name,    
#             sap.program,
#             sap.min_age,
#             sap.max_age
#         FROM
#             `tabStudent Admission` AS sa
#         JOIN
#             `tabStudent Admission Program` AS sap
#         ON
#             sa.name = sap.parent
#         WHERE
#             sa.academic_year = %s
#             AND sap.program = %s
#     """, (academic_year, program), as_dict=1)

#     return result
