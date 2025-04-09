frappe.ui.form.on('Visitor Management System', {
    validate: function (frm) {
        if (!frm.doc.cnicpassport_no) {
            frappe.throw("Please enter CNIC/Passport number.");
        }
    }
});
