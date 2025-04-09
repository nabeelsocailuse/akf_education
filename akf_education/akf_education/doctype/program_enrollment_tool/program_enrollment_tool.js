// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Program Enrollment Tool', {
  setup: function (frm) {
    frm.add_fetch('student', 'title', 'student_name')
    frm.add_fetch('student_applicant', 'title', 'student_name')
    if (frm.doc.__onload && frm.doc.__onload.academic_term_reqd) {
      frm.toggle_reqd('academic_term', true)
    }   
    console.log("Here is my Program enrollment tool") 
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
    })

    frm.add_fetch(
      frm.doc.academic_term ? 'new_academic_term' : 'new_academic_year',
      frm.doc.academic_term ? 'term_start_date' : 'year_start_date',
      'enrollment_date'
    )
    
    let value = frm.doc.aghosh_home1;
    console.log("Current value of aghosh_home1:", value);
  
    // if (frm.doc.students && frm.doc.students.length > 0) {
    //     frm.doc.students.forEach(row => {
    //         console.log("Student Name: " + row.bed);
    //     });
    // } else {
    //     console.log("No students found in the child table.");
    // }
  
    // Set query for bed field in the child table
    frm.fields_dict["students"].grid.get_field("bed").get_query = function(doc, cdt, cdn) {
        return {
            filters: {
                "occupied_status": "Vacant",
                "aghosh_home": doc.aghosh_home1  // Ensuring beds belong to the selected home
            }
        };
    };

    frm.fields_dict["students"].grid.get_field("external").get_query = function(doc, cdt, cdn) {
      return {
          filters: {
              "aghosh_home": doc.aghosh_home1  // Ensuring beds belong to the selected home
          }
      };
  };



// This can be shown while saving data
  //   frm.doc.students.forEach(row => {
  //     console.log("School Type:", row.school_type1);
  // });



frappe.ui.form.on("Program Enrollment Tool Student", {
  school_type1: function(frm, cdt, cdn) {
      let row = locals[cdt][cdn];
      console.log("Changed School Type:", row.school_type1);
      let values = frm.doc.internal

      if (row.school_type1 === "Internal") {
          frappe.call({
              method: 'akf_education.akf_education.doctype.program_enrollment_tool.program_enrollment_tool.get_buildings_by_aghosh_home',

              args: {
                  aghosh_home1: frm.doc.aghosh_home1
              },
              callback: function (r) {
                  if (r.message) {
                      console.log("My data", r.message);
                      frappe.model.set_value(cdt, cdn, 'internal', r.message.name); 
                  }
              }
          });
      } else if (row.school_type1 === "External"){

        frappe.model.set_value(cdt,cdn, 'internal', '')
      }
  },

  donor_list: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn]; // Get current row in child table
    let selected_donors = [];

    let dialog = new frappe.ui.Dialog({
        title: "Select Donors",
        fields: [
            {
                label: "Select Donor",
                fieldname: "donor_filter",
                fieldtype: "Link",
                options: "Donor",
                get_query: function () {
                    return {
                        filters: [["name", "not in", selected_donors.map(d => d.id)]]
                    };
                },
                onchange: function () {
                    let donor_id = dialog.get_value("donor_filter");
                    if (donor_id && !selected_donors.some(donor => donor.id === donor_id)) {
                        frappe.db.get_value("Donor", donor_id, "name", function (r) {
                            if (r && r.name) {
                                selected_donors.push({ id: donor_id, name: r.name });
                                dialog.set_value("donor_filter", "");
                                update_donor_table(); 
                                refresh_field("donor_filter");
                            }
                        });
                    }
                }
            },
            {
                label: "Donor List",
                fieldname: "donor_table",
                fieldtype: "Table",
                cannot_add_rows: true,
                in_place_edit: false,
                fields: [
                    { fieldtype: "Data", fieldname: "name", label: "Donor Name", in_list_view: 1 }
                ]
            }
        ],
        primary_action_label: "Select",
        primary_action(values) {
            // Save selected donors to the child doctype field
            frappe.model.set_value(cdt, cdn, "selected_donors", selected_donors.map(d => d.name).join(", "));

            dialog.hide();
        }
    });

    function update_donor_table() {
        dialog.set_df_property("donor_table", "data", selected_donors);
        dialog.refresh_field("donor_table");
    }

    dialog.show();
}
});

  },

  get_students_from: function (frm) {
    if (frm.doc.get_students_from == 'Student Applicant') {
      frm.dashboard.add_comment(
        __(
          'Only the Student Applicant with the status "Approved" will be selected in the table below.'
        )
      )
    }
  },

  
  get_students: function (frm) {
    frm.set_value('students', [])
    frappe.call({
      method: 'get_students',
      doc: frm.doc,
      callback: function (r) {
        if (r.message) {
          frm.set_value('students', r.message)
        }
      },
    })
  },

  enroll_students: function (frm) {

    frappe.call({
      method: 'enroll_students',
      doc: frm.doc,
      callback: function (r) {
        frm.set_value('students', [])
        // frappe.show_alert({
        //   message:__('Students Enrolled Successfully!'),
        //   indicator:'green'
        // },5);
        frappe.hide_msgprint(true)
        frm.reload_doc();
      },
    })
  },

  academic_term: function (frm) {
    frm.refresh()
  },

})



















































