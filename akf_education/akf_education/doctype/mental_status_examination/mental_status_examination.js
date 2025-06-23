// Copyright (c) 2025, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mental Status Examination", {
	refresh(frm) {
        frm.set_query("student_id", function () {
			return {
				filters: {
					status: "Active"
				},
			};
		});
	},
});
