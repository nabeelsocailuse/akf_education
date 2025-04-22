// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Building", {
    refresh: function(frm) {
        toggle_principle_field(frm);
       
    },
    type: function(frm) {
        toggle_principle_field(frm);
        clear_type_specific_fields(frm);
    }
});

function toggle_principle_field(frm) {
    if (frm.doc.type === "School") {
        frm.set_df_property("principal_id", "reqd", 1);
        frm.toggle_display("principal_id", true); 
    } else {
        frm.set_df_property("principal_id", "reqd", 0);
        frm.toggle_display("principal_id", false); 
    }
}

function clear_type_specific_fields(frm) {
    if (frm.doc.type === "School") {
        frm.set_value("building_name", null);
    } else if (frm.doc.type === "Hostel") {
        frm.set_value("name_of_school", null);
    } else {
        // Clear both if type is something else
        frm.set_value("building_name", null);
        frm.set_value("name_of_school", null);
    }
}
