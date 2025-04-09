frappe.ui.form.on('Visitor Management System', {
    validate: function (frm) {
        return new Promise((resolve, reject) => {
            if (!frm.doc.cnicpassport_no) {
                frappe.throw("Please enter CNIC/Passport number.");
                reject();
                return;
            }

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Guardian",
                    filters: {
                        cnic_number: frm.doc.cnicpassport_no
                    },
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        frappe.show_alert({
                            message:__('Guarian Found! '),
                            indicator:'green'
                        }, 5);
                        resolve();
                    } else {
                        frappe.msgprint({
                            title: "Guardian Status",
                            message: "❌ Guardian not available. Cannot save this entry.",
                            indicator: "red"
                        });
                        reject();
                    }
                }
            });
        });
    }

});

frappe.ui.form.on('Visitor Management System', {
    validate: function(frm) {
        if (frm.doc.cnicpassport_no) {
            frappe.call({
                method: 'akf_education.akf_education.doctype.visitor_management_system.test_visitor_management_system.guardian_details',
                args: {
                    cnic_number: frm.doc.cnicpassport_no
                },
                callback: function(r) {
                    if (r.message) {
                        frm.fields_dict.guardian_info.$wrapper.html(r.message);
                    }
                }
            });
        }
    }
});

