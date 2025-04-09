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
                            message: __('✅ Guardian Found!'),
                            indicator: 'green'
                        }, 5);

                        frappe.call({
                            method: "akf_education.akf_education.doctype.visitor_management_system.visitor_management_system.guardian_details",
                            args: {
                                cnic_number: frm.doc.cnicpassport_no,
                                parent_docname: frm.doc.name  
                            },
                            callback: function (res) {
                                if (res.message) {
                                    frappe.msgprint(res.message); 
                                    resolve(); 
                                }
                            }
                        });
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