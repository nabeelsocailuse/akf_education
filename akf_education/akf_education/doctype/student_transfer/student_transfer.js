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
    student_id: function(frm) {
        frm.refresh_fields([
                    "student_name",
                    "current_aghosh_home_id",
                    "current_aghosh_home_name",
                    "current_building_id",
                    "current_building_name",
                    "current_room_id",
                    "current_room_number",
                    "current_bed_id",
                    "current_bed_number"
                ]);
        frappe.call({
            method: "get_program_enrollment",
            doc: frm.doc,
            callback: function(r) {
            }
        });
    },
    school_type: function(frm) {
        if (frm.doc.school_type === "Internal") {
            frm.set_value("external_school", "");
            frm.set_value("external_school_name", "");
        } else if (frm.doc.school_type === "External") {
            frm.set_value("internal_school", "");
            frm.set_value("external_school_name", "");
        }
    },
    transfer_type: function(frm) {
        frappe.call({
            method: "prefill_transfer_scenario",
            doc: frm.doc,
            callback: function(r) {
                frm.refresh_fields([
                    "new_aghosh_home_id",
                    "new_aghosh_home_name",
                    "new_building_id",
                    "new_building_name",
                    "new_room_id",
                    "new_room_number",
                    "new_bed_id",
                    "new_bed_number"
                ]);
            }
        });
    }
})