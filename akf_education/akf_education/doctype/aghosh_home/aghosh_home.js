frappe.ui.form.on("Aghosh Home", {
    refresh: function (frm) {
		frm.set_query("district", function () {
			return {
				filters: {
					region: frm.doc.region,
				},
			};
		});

		frm.set_query("tehsil", function () {
			return {
				filters: {
					district: frm.doc.district,
				},
			};
		});
		frm.set_query("employee_id", function () {
			return {
				filters: {
					branch: frm.doc.branch,
				},
			};
		});
		frm.set_query('branch', function() {
            return {
                filters: [
                    ['name', 'like', 'Aghosh%']
                ]
            };
        });
	},
    // region: function(frm) {
    //     if (frm.doc.region) {
    //         updateOptions(frm, frm.doc.region, frm.doc.district);
    //     }
    // },

    // district: function(frm) {
    //     if (frm.doc.district) {
    //         updateOptions(frm, frm.doc.region, frm.doc.district);
    //     }
    // }
});

// function updateOptions(frm, region, district) {
//     frappe.call({
//         method: "akf_education.akf_education.doctype.aghosh_home.aghosh_home.get_region_and_tehsil",
//         args: {
//             region: region,
//             district: district
//         },
//         callback: function(r) {
//             if (r.message) {
//                 if (r.message.districts) {
//                     frm.district_list = r.message.districts.map(row => row.district_name);
//                     frm.set_query('district', function() {
//                         return {
//                             filters: [
//                                 ['name', 'in', frm.district_list]
//                             ]
//                         };
//                     });
//                     frm.refresh_field('district');
//                 }

//                 if (r.message.tehsils) {
//                     frm.tehsil_list = r.message.tehsils.map(row => row.tehsil_name);
//                     frm.set_query('tehsil', function() {
//                         return {
//                             filters: [
//                                 ['name', 'in', frm.tehsil_list]
//                             ]
//                         };
//                     });
//                     frm.refresh_field('tehsil');
//                 }
//             }
//         }
//     });
// }
