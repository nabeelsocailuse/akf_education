// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Beds", {
        refresh: function(frm) {
            frm.set_query('aghosh_home_id', function() {
            return {
                filters: {
                    "status": "Operational"
                    }
                };
            });
                
            frm.set_query("building", function() {
                return {
                    filters: {
                        aghosh_home_id: frm.doc.aghosh_home_id,
                        type: "Hostel",
                        "status": "Active"
                    }
                };
            });
                frm.set_query('room_id', () => {
                    return {
                        filters: {
                            aghosh_home_id: frm.doc.aghosh_home_id,
                            building: frm.doc.building
                    }
                    };
                });
            }
});
