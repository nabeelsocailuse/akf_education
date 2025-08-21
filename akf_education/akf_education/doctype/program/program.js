// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Program", {
    refresh: function (frm) {
        frm.set_query("aghosh_home_id", function () {
            return {
                filters: {
                    status: "Operational"
                },
            };
        });

        frm.set_query('external_school_id', function () {
            return {
                Filters: {
                    aghosh_home_id: frm.doc.aghosh_home_id,
                },
            };
        });

        frm.set_query("internal_school_id", function () {
            return {
                Filters: {
                    aghosh_home_id: frm.doc.aghosh_home_id,
                },
            };
        });
    },

    validate: function (frm) {
        let seen = new Set();
        for (let row of frm.doc.courses) {
            if (seen.has(row.course)) {
                frappe.throw(`Duplicate entry: ${row.course} in Courses`);
            }
            seen.add(row.course);
        }
    }
});