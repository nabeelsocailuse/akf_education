// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Promote Student", {
    refresh(frm) {
        frm.set_query("aghosh_home_id", function () {
            return {
                filters: {
                    status: "Operational"
                },
            };
        });

        frm.set_query("program", function () {
            return {
                filters: {
                    aghosh_home_id: frm.doc.aghosh_home_id,
                },
            };
        });

        frm.set_query("new_program", function () {
            return {
                filters: {
                    aghosh_home_id: frm.doc.aghosh_home_id,
                },
            };
        });
    },

    get_students: function (frm) {
        frm.set_value('students', []);
        frappe.call({
            method: 'get_students',
            doc: frm.doc,
            callback: function (r) {
                if (r.message) {
                    frm.set_value('students', r.message)
                }
            },
        });
    },

    promote_to_new_class: function (frm) {
        frappe.call({
            method: 'promote_students',
            doc: frm.doc,
            callback: function (r) {
                // frm.set_value('students', [])
                frappe.hide_msgprint(true)
                frm.reload_doc();
            },
        });
    },

});
