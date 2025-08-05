# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
# from datetime import timedelta, datetime
from frappe import msgprint, _


# @frappe.whitelist(allow_guest=True)
def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [
        _("Child ID") + ":Link/Student:140",
        _("Child Name") + ":Data:140",
        _("Incident") + ":Data:140",
        _("Incident Date") + ":Date:140",
        _("Showcause Issue Date") + ":Date:140",
    ]
    return columns


def get_data(filters):
    result = get_query_result(filters)
    return result


def get_conditions(filters):
    conditions = ""

    # if filters.get("company"):
    #     conditions += " AND company = %(company)s"
    # if filters.get("applicant"):
    #     conditions += " AND applicant = %(applicant)s"
    # if filters.get("branch"):
    #     conditions += " AND branch = %(branch)s"
    # if filters.get("loan_type"):
    #     conditions += " AND loan_type = %(loan_category)s"
    # if filters.get("repayment_start_date"):
    #     conditions += " AND repayment_start_date = %(repayment_start_date)s"

    return conditions


def get_query_result(filters):
    conditions = get_conditions(filters)
    result = frappe.db.sql(
        """
        SELECT 
            affected_person,
            affected_person_name,
            incident_type,
            incident_date_time,
            closure_date
        FROM 
            `tabIncident Report`
        WHERE
            docstatus != 2
        {0}
    """.format(
            conditions if conditions else ""
        ),
        filters,
        as_dict=0,
    )
    return result