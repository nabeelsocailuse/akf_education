// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student Admission Tool", {
    onload: function (frm) {
    if (!frm.is_new()) {
      // Clear fields
      frm.set_value('region', '');
      frm.set_value('district', '');
      frm.set_value('academic_year', '');
      frm.set_value('admission_start_date', '');
      frm.set_value('admission_end_date', '');
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
					region: frm.doc.region,
				},
			};
		});
       
    }
});

function get_aghosh_homes(frm) {
    frappe.call({
        method: 'akf_education.akf_education.doctype.student_admission_tool.student_admission_tool.get_aghosh_homes',
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
