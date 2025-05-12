// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("External School", {
	refresh: function (frm) {
		frm.set_query("district", function () {
			return {
				filters: {
					region: frm.doc.region,
				},
			};
		});

		frm.set_query("tehsil", function () {
			return {
				filters: {
					district: frm.doc.district,
				},
			};
		});
		frm.set_query("employee_id", function () {
			return {
				filters: {
					branch: frm.doc.branch,
				},
			};
		});
		frm.set_query('branch', function() {
            return {
                filters: [
                    ['name', 'like', 'Aghosh%']
                ]
            };
        });
		frm.set_query('aghosh_home_id', function() {
            return {
                filters: {
					"status": "Operational"
				}
            };
        });
	},
});
