# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    return get_columns(), get_data(filters or {})

def get_columns():
    return [
        {'fieldname': "orphan_id", 'label': 'Student ID', 'fieldtype': 'Data', 'width': 180},
        {"fieldname": "orphan_name", "label": "Orphan Name", "fieldtype": "Data", "width": 150},
        {'fieldname': 'donor_id', 'label': 'Donor ID', 'fieldtype': 'Link', "options": "Donor", 'width': 190},
        {'fieldname': 'donor_name', 'label': 'Donor Name', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'sponsorship_tenure', 'label': 'Sponsorship Tenure', 'fieldtype': 'Data', 'width': 150},
        {'fieldname': 'tenure_period', 'label': 'Tenure Period', 'fieldtype': 'Float', 'width': 150},
        {'fieldname': 'start_date', 'label': 'Start Date', 'fieldtype': 'Date', 'width': 150},
        {'fieldname': 'end_date', 'label': 'End Date', 'fieldtype': 'Date', 'width': 150},
    ]

def get_data(filters):
    conditions = "tenure_period > 0" 
    values = {}

    if filters.get("orphan_id"):
        conditions += " AND orphan_id = %(orphan_id)s"
        values["orphan_id"] = filters["orphan_id"]

    if filters.get("donor_id"):
        conditions += " AND donor_id = %(donor_id)s"
        values["donor_id"] = filters["donor_id"]

    if filters.get("sponsorship_tenure"):
        conditions += " AND sponsorship_tenure = %(sponsorship_tenure)s"
        values["sponsorship_tenure"] = filters["sponsorship_tenure"]

    if filters.get("tenure_period") is not None:
        tenure_period = float(filters["tenure_period"])
        conditions += " AND tenure_period >= %(tenure_period)s"
        values["tenure_period"] = tenure_period

    return frappe.db.sql(f"""
        SELECT orphan_id, orphan_name, donor_id, donor_name, sponsorship_tenure, tenure_period, start_date, end_date
        FROM `tabSponsorship`
        WHERE {conditions}
    """, values, as_dict=True)


