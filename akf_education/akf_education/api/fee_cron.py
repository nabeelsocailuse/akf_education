import frappe
from frappe.utils import nowdate, get_first_day, getdate, add_months

@frappe.whitelist()
def generate_monthly_fees():
    today = nowdate()
    current_month_start = get_first_day(today)

    academic_years = frappe.get_all("Academic Year", filters={"year_end_date": [">=", today]}, fields=["name", "year_end_date"])

    for year in academic_years:
        # Get all Fees under this academic year that need to be duplicated
        fee_records = frappe.get_all("Fees", filters={
            "academic_year": year.name,
            "docstatus": 1  # submitted
        }, fields=["name", "student", "due_date", "posting_date", "academic_term"])

        for fee in fee_records:
            # Optional: Prevent duplicate generation
            exists = frappe.get_all("Fees", filters={
                "student": fee.student,
                "academic_year": year.name,
                "posting_date": current_month_start
            })

            if not exists:
                new_fee = frappe.copy_doc(frappe.get_doc("Fees", fee.name))
                new_fee.posting_date = current_month_start
                new_fee.due_date = add_months(fee.due_date, 1)
                new_fee.insert()
                new_fee.submit()
