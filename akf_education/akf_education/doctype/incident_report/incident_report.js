// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Incident Report", {
    refresh: function (frm) {
        frm.set_query("affected_person", function () {
            return {
                filters: {
                    "status": 'Active',
                },
            };

        });

        // 	onload: function(frm) {
        //         if (!frm.doc.closure_date) {
        //             frm.set_value('closure_date', frappe.datetime.now_datetime());
        //         }
        //     }
    }
});
