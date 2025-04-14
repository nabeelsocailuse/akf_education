// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Aghosh Home", {
    district: function(frm) {
        if (frm.doc.district) {
            updateTehsilOptions(frm, frm.doc.district);
        }
    }

});


function updateTehsilOptions(frm, district) {
    frappe.call({
        method: "akf_education.akf_education.doctype.aghosh_home.aghosh_home.get_tehsils_by_district", 
        args: {
            district: district 
        },
        callback: function(r) {
            if (r.message) {
                // Save the tehsil list into frm.tehsil_list
                frm.tehsil_list = r.message.map(row => row.tehsil_name);

                // Set a custom query for tahsil field
                frm.set_query('tahsil', function() {
                    return {
                        filters: [
                            ['name', 'in', frm.tehsil_list]
                        ]
                    };
                });

                // OPTIONAL: if you want to refresh field immediately
                frm.refresh_field('tahsil');
            }
        }
    });
}










