// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.query_reports["Sponsorship Details"] = {
	"filters": [
		{
            "fieldname": "student_id",
            "fieldtype": "Link",
            "label": "Student ID",
			"options": "Student",
            "reqd": 0,
        },

		{
			"fieldname": "donor_id",
			"label": "Donor ID",
			"fieldtype": "Link",
			"options": "Donor",
			"reqd": 0			
		},

        {
			"fieldname": "sponsorship_tenure",
			"label": "Sponsorship Tenure",
			"fieldtype": "Select",
			"options": "\nMonthly\nQuarterly\nYearly",
			"reqd": 0
		},		

		{
			"fieldname": "tenure_period",
    		"label": "Tenure Period",
    		"fieldtype": "Float",
    		"reqd": 0
		},
	]
};
