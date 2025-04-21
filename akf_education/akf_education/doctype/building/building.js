// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Building", {
    refresh: function(frm) {
        toggle_principle_field(frm);
    },
    type_enum: function(frm) {
        toggle_principle_field(frm);
    }
});

function toggle_principle_field(frm) {
    if (frm.doc.type === "School") {
        frm.set_df_property("principle_name", "reqd", 1);
        frm.toggle_display("principle_name", true); 
    } else {
        frm.set_df_property("principle_name", "reqd", 0);
        frm.toggle_display("principle_name", false); 
    }
}

