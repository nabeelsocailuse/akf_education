// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rooms", {
    refresh: function(frm) {
        frm.set_query("building", function() {
            return {
                filters: {
                    aghosh_home_id: frm.doc.aghosh_home
                }
            };
        });
    }
});

