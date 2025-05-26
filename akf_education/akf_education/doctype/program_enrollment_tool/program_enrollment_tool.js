// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Program Enrollment Tool', {
  onload: function (frm) {
    if (!frm.is_new()) {
      // Clear fields
      frm.set_value('program', '');
      frm.set_value('aghosh_home_id', '');
      frm.set_value('aghosh_home_name', '');
      // Clear child table
      frm.set_value('students', []);
      frm.set_value('sponsors', []);
    }
  },
  setup: function (frm) {
    frm.add_fetch('student', 'title', 'student_name')
    frm.add_fetch('student_applicant', 'title', 'student_name')
    if (frm.doc.__onload && frm.doc.__onload.academic_term_reqd) {
      frm.toggle_reqd('academic_term', true)
    }
  },

  refresh: function (frm) {
    // frm.disable_save()
    frm.fields_dict.enroll_students.$input.addClass(' btn btn-primary')
    frappe.realtime.on('program_enrollment_tool', function (data) {
      frappe.hide_msgprint(true)
      frappe.show_progress(
        __('Enrolling students'),
        data.progress[0],
        data.progress[1]
      )
    });

    frm.add_fetch(
      frm.doc.academic_term ? 'new_academic_term' : 'new_academic_year',
      frm.doc.academic_term ? 'term_start_date' : 'year_start_date',
      'enrollment_date'
    );
  
  // Set queries for fields in the child table
  frm.fields_dict["students"].grid.get_field("building").get_query = function (doc, cdt, cdn) {
    return {
      filters: {
        "aghosh_home_id": doc.aghosh_home_id,
        "type": "Hostel"
      }
    };
  };

  frm.fields_dict["students"].grid.get_field("internal_school").get_query = function (doc, cdt, cdn) {
    return {
      filters: {
        "aghosh_home_id": doc.aghosh_home_id,
        "type": "School"
      }
    };
  };

  frm.fields_dict["students"].grid.get_field("room").get_query = function (doc, cdt, cdn) {
    let row = locals[cdt][cdn];
    return {
      filters: {
        "aghosh_home_id": doc.aghosh_home_id,
        "building":row.building,
        "occupied_status": "Vacant"
      }
    };
  };
  
  frm.fields_dict["students"].grid.get_field("bed").get_query = function (doc, cdt, cdn) {
    let row = locals[cdt][cdn];
    return {
      filters: {
        "aghosh_home_id": doc.aghosh_home_id,
        "occupied_status": "Vacant",
        "room_id": row.room

      }
    };
  };

  frm.fields_dict["students"].grid.get_field("external_school").get_query = function (doc, cdt, cdn) {
    return {
      filters: {
        "aghosh_home_id": doc.aghosh_home_id
      }
    };
  };
},


  // get_students_from: function (frm) {
  //   if (frm.doc.get_students_from == 'Student Applicant') {
  //     frm.dashboard.add_comment(
  //       __(
  //         'Only the Student Applicant with the status "Approved" will be selected in the table below.'
  //       )
  //     )
  //   }
  // },

  
  get_students: function (frm) {
    frm.set_value('students', []);
    frm.set_value('sponsors', []);
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
  enroll_students: function (frm) {
    frappe.call({
      method: 'enroll_students',
      doc: frm.doc,
      callback: function (r) {
        frm.set_value('students', [])
        frappe.hide_msgprint(true)
        frm.reload_doc();
      },
    });
  },
  // frappe.show_alert({
        //   message:__('Students Enrolled Successfully!'),
        //   indicator:'green'
        // },5);

  // academic_term: function (frm) {
  //   frm.refresh()
  // },

});


// Events for child table `Program Enrollment Tool Student`
frappe.ui.form.on("Program Enrollment Tool Student", {
  create_sponsorship: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let dialog = new frappe.ui.Dialog({
            title: 'Add Donors',
            fields: [
                {
                    label: 'Donors',
                    fieldname: 'donor_list',
                    fieldtype: 'MultiSelectList',
                    get_data: async () => {
                        let donors = await frappe.db.get_list('Donor', {
                            fields: ['name']
                        });
                        return donors.map(d => d.name);
                    },
                    reqd: true
                }
            ],
            primary_action_label: 'Insert Donors',
            primary_action(values) {
                if (values.donor_list && values.donor_list.length) {
                    values.donor_list.forEach(donor_name => {
                        let child = frm.add_child('sponsors');
                        child.donor_id = donor_name;
                        child.student_applicant = row.student_applicant;
                        child.applicant_name = row.student_name;
                    });

                    frm.refresh_field('sponsors');
                    frm.dirty();
                    dialog.hide();
                } else {
                    frappe.msgprint(__('Please select at least one donor'));
                }
            }
        });

        dialog.show();
      }
  // school_type: function (frm, cdt, cdn) {
  //   let row = locals[cdt][cdn];

  //   if (row.school_type === "internal_school") {
  //     frappe.call({
  //       method: 'akf_education.akf_education.doctype.program_enrollment_tool.program_enrollment_tool.get_buildings_by_aghosh_home',
  //       args: {
  //         aghosh_home_id: frm.doc.aghosh_home_id
  //       },
  //       callback: function (r) {
  //         if (r.message) {
  //           frappe.model.set_value(cdt, cdn, 'internal_school', r.message.name);
  //         }
  //       }
  //     });
  //   } else if (row.school_type === "external_school") {
  //     frappe.model.set_value(cdt, cdn, 'internal_school', '');
  //   }
  // },

//   donor_list: function (frm, cdt, cdn) {
//     let selected_donors = [];
//     let dialog = new frappe.ui.Dialog({
//       title: "Select Donors",
//       fields: [
//         {
//           label: "Select Donor",
//           fieldname: "donor_filter",
//           fieldtype: "Link",
//           options: "Donor",
//           get_query: function () {
//             return {
//               filters: [["name", "not in", selected_donors.map(d => d.id)]]
//             };
//           },
//           onchange: function () {
//             let donor_id = dialog.get_value("donor_filter");
//             if (donor_id && !selected_donors.some(donor => donor.id === donor_id)) {
//               frappe.db.get_value("Donor", donor_id, "name", function (r) {
//                 if (r && r.name) {
//                   selected_donors.push({ id: donor_id, name: r.name });
//                   dialog.set_value("donor_filter", "");
//                   update_donor_table();
//                   refresh_field("donor_filter");
//                 }
//               });
//             }
//           }
//         },
//         {
//           label: "Donor List",
//           fieldname: "donor_table",
//           fieldtype: "Table",
//           cannot_add_rows: true,
//           in_place_edit: false,
//           fields: [
//             { fieldtype: "Data", fieldname: "name", label: "Donor Name", in_list_view: 1 }
//           ]
//         }
//       ],
//       primary_action_label: "Select",
//       primary_action(values) {
//         frappe.model.set_value(cdt, cdn, "selected_donors", selected_donors.map(d => d.name).join(", "));
//         dialog.hide();
//       }
//     });

//     function update_donor_table() {
//       dialog.set_df_property("donor_table", "data", selected_donors);
//       dialog.refresh_field("donor_table");
//     }

//     dialog.show();
//   }
});
