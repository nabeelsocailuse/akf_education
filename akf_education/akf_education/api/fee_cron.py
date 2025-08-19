# import frappe
# from frappe.utils import nowdate, get_first_day, getdate, add_months

# @frappe.whitelist()
# def generate_monthly_fees():
#     today = nowdate()
#     current_month_start = get_first_day(today)

#     academic_years = frappe.get_all("Academic Year", filters={"year_end_date": [">=", today]}, fields=["name", "year_end_date"])

#     for year in academic_years:
#         # Get all Fees under this academic year that need to be duplicated
#         fee_records = frappe.get_all("Fees", filters={
#             "academic_year": year.name,
#             "docstatus": 1  # submitted
#         }, fields=["name", "student", "due_date", "posting_date", "academic_term"])

#         for fee in fee_records:
#             # Optional: Prevent duplicate generation
#             exists = frappe.get_all("Fees", filters={
#                 "student": fee.student,
#                 "academic_year": year.name,
#                 "posting_date": current_month_start
#             })

#             if not exists:
#                 new_fee = frappe.copy_doc(frappe.get_doc("Fees", fee.name))
#                 new_fee.posting_date = current_month_start
#                 new_fee.due_date = add_months(fee.due_date, 1)
#                 new_fee.insert()
#                 new_fee.submit()


import frappe
from frappe.utils import nowdate, get_first_day, get_last_day

@frappe.whitelist()
def create_monthly_fees():
    today = nowdate()
    posting_date = get_first_day(today)
    due_date = get_last_day(today)

    enrollments = frappe.get_all(
        "Program Enrollment",
        filters={
            "active": 1,
            "school_type": "External"
        },
        fields=[
            "name",
            "student",
            "student_name",
            "program"
        ]
    )
    # frappe.throw(f"Enrollments found: {enrollments}")

    for enr in enrollments:
        # (1) Double-check Student Doc Status
        student_status = frappe.db.get_value("Student", enr.student, "status")
        if student_status != "Active":
            continue

        # frappe.throw(f"Processing enrollment for {enr.student} in program {enr.program}")

        # (2) Avoid duplicate fee creation for same month
        exists = frappe.db.exists(
            "Fees",
            {
                "student": enr.student,
                "posting_date": posting_date,
                "program": enr.program
            }
        )

        if exists:
            continue

        # (3) Create Fee Doc
        fee = frappe.new_doc("Fees")
        fee.program_enrollment = enr.name
        fee.student = enr.student
        fee.student_name = enr.student_name
        fee.program = enr.program
        fee.posting_date = posting_date
        fee.due_date = due_date

        # frappe.throw(f"enr: {enr.name}, student: {enr.student}, program: {enr.program}")

        # (4) Pull Fee components from child table of Program Enrollment
        childtable = frappe.get_doc("Program Enrollment", enr.name)
        frappe.msgprint(f"Child table components: {childtable.components}")
        for row in childtable.components:  # ensure your child table fieldname is 'fees'
            fee.append("components", {
                "fees_category": row.fees_category,
                "amount": row.amount
            })

        fee.insert()
        # fee.submit()

        frappe.logger().info(f"Created monthly fee for {enr.student} ({posting_date})")
