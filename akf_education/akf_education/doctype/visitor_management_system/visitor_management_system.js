frappe.ui.form.on('Visitor Management System', {
    validate: function (frm) {
        if (!frm.doc.cnicpassport_no) {
            frappe.throw("Please enter CNIC/Passport number.");
        }

        if (!frm.doc.purpose_of_visit) {
            frappe.throw("Please select purpose of visit.");
        }
    },

    purpose_of_visit: function (frm) {
        if (frm.doc.purpose_of_visit === "Meeting Resident") {
            frm.set_df_property("table", "hidden", 0); 
        } else {
            frm.clear_table("table");                  
            frm.set_df_property("table", "hidden", 1); 
            frm.refresh_field("table");               
        }
    },

    onload: function (frm) {
        if (frm.doc.purpose_of_visit !== "Meeting Resident") {
            frm.set_df_property("table", "hidden", 1); 
        }
    }
});

