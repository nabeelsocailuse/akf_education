frappe.ui.form.on('Visitor Management System', {
    validate: function (frm) {
        if (!frm.doc.cnicpassport_no) {
            frappe.throw("Please enter CNIC/Passport number.");
        }
    },

    validate: function (frm) {
        if (!frm.doc.purpose_of_visit){
            frappe.throw("Please select purpose of visit")
        }
    }
});
 