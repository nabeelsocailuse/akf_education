frappe.ui.form.on("Student Transfer", {
    refresh: function(frm) {
        frm.set_query("student_id", function() {
            return {
                filters: {
                    "status": "Active"
                }
            };
        });

        frm.set_query("new_building_id", function() {
            return {
                filters: {
                    "aghosh_home_id": frm.doc.new_aghosh_home_id,
                    "type": "Hostel"
                }
            };
        });

        frm.set_query("new_room_id", function() {
            return {
                filters: {
                    "aghosh_home_id": frm.doc.new_aghosh_home_id,
                    "building": frm.doc.new_building_id
                }
            };
        });

        frm.set_query("new_bed_id", function() {
            return {
                filters: {
                    "aghosh_home_id": frm.doc.new_aghosh_home_id,
                    "building": frm.doc.new_building_id,
                    "room_id": frm.doc.new_room_id
                }
            };
        });

        frm.set_query("internal_school", function() {
            return {
                filters: {
                    "aghosh_home_id": frm.doc.new_aghosh_home_id,
                    "type": "School"
                }
            };
        });

        frm.set_query("external_school", function() {
            return {
                filters: {
                    "aghosh_home_id": frm.doc.new_aghosh_home_id
                }
            };
        });
    },
    transfer_type: function(frm) {
        frappe.call({
            method: "akf_education.akf_education.doctype.student_transfer.student_transfer.prefill_transfer_scenario",
            args: {},
            callback: function(r) {
                if (r.message) {
                }
            }
        });
    }
})