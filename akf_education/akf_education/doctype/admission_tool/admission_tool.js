// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Admission Tool", {
    refresh(frm) {
        frm.add_custom_button('Get Aghosh Homes', function () {
            get_aghosh_homes(frm);
        });

        frm.add_custom_button('Create Admissions', function () {
            create_admissions_func(frm);
        });
    }
});

function get_aghosh_homes(frm) {
    frappe.call({
        method: 'akf_education.akf_education.doctype.admission_tool.admission_tool.get_aghosh_homes',
        type: "GET",
        args: {
            'filters': { 
                'region': frm.doc.region,
                'district': frm.doc.district
            },
        },
        callback: function (r) {
            if (!r.exc) {
                const data = r.message;
                frm.set_value('admission_table', data);
            }
        }
    });
}
function create_admissions_func(frm){
    frm.call("create_admissions");
}
