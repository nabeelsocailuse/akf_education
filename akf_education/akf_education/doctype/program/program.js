// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Program", {
    validate: function(frm) {
        let seen = new Set();
        for (let row of frm.doc.courses) {
            if (seen.has(row.course)) {
                frappe.throw(`Duplicate entry: ${row.course} in Courses`);
            }
            seen.add(row.course);
        }
    }
});