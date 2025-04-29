// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Beds", {
        refresh: function(frm) {
                frm.set_query('room_id', () => {
                    return {
                        filters: [
                            ['Rooms', 'school_name', '=', '']
                        ]
                    };
                });
            }
});
