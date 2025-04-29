// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student Activities", {
    refresh: function(frm) {
        frm.set_query("student_id", function() {
            return {
                filters: {
                    aghosh_home_id: frm.doc.aghosh_home_id
                }
            };
        });
    }
});

