// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Admission Tool", {
    validate: function(frm) {
        let admission_start_date = frm.doc.admission_start_date;
        let admission_end_date = frm.doc.admission_end_date;
        let today = frappe.datetime.get_today();

        if (admission_start_date && admission_end_date < today) {
            frappe.throw(__('Date must be today or later.'));
        }
    },

    onload: function (frm) {
    if (!frm.is_new()) {
      // Clear fields
      frm.set_value('region', '');
      frm.set_value('district', '');
      // Clear child table
      frm.set_value('admission_table', []);
    }
  },
    refresh(frm) {
        frm.add_custom_button('Get Aghosh Homes', function () {
            get_aghosh_homes(frm);
        });

        frm.add_custom_button('Create Admissions', function () {
            create_admissions_func(frm);
        });
        frm.set_query("district", function () {
			return {
				filters: {
					custom_region: frm.doc.region,
				},
			};
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
