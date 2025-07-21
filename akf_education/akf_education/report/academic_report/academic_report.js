// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.query_reports["Academic Report"] = {
	"filters": [
		{
			"fieldname":"aghosh_home_id",
			"label": __("Aghosh Home ID"),
			"fieldtype": "Link",
			"options": "Aghosh Home"
		},
		// {
		// 	"fieldname":"status",
		// 	"label": __("Status"),
		// 	"fieldtype": "Select",
		// 	"options": [
		// 		{"value": "0", "label": __("Draft")},
		// 		{"value": "1", "label": __("Submitted")},
		// 	]
		// },
		{
			"fieldname":"percentage",
			"label": __("Percentage"),
			"fieldtype": "Select",
			"options": [
				{"value": "0", "label": __("All")},
				{"value": "1", "label": __("Above 75%")},
				{"value": "2", "label": __("Below 75%")},
			]
		},
		{
			"fieldname":"academic_year",
			"label": __("Academic Year"),
			"fieldtype": "Link",
			"options": "Academic Year",
		},
		{
			"fieldname":"program",
			"label": __("Class"),
			"fieldtype": "Link",
			"options": "Program"
		},
	]
};
