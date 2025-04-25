// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student', {
  refresh: function (frm) {
    frm.set_query('user', function (doc) {
      return {
        filters: {
          ignore_user_type: 1,
        },
      }
    })

// Accounting Leger Button Commented
    // if (!frm.is_new()) {
    //   frm.add_custom_button(__('Accounting Ledger'), function () {
    //     frappe.set_route('query-report', 'General Ledger', {
    //       party_type: 'Customer',
    //       party: frm.doc.customer,
    //     })
    //   })
    // }




    
    // frappe.db
    //   .get_single_value('Education Settings', 'user_creation_skip')
    //   .then((r) => {
    //     if (cint(r) !== 1) {
    //       frm.set_df_property('student_email_id', 'reqd', 1)
    //     }
    //   })

  },

  setup: function (frm) {
    if (frm.doc.student_applicant) {
      set_guardians_from_applicant(frm);
      setTimeout(() => {
        frm.save();
      }, 250);
    }   
  },
  
 

  student_applicant:function(frm){
    calculate_age(frm);
    set_guardians_from_applicant(frm);

  },

    date_of_birth1: function(frm) {
      calculate_age(frm);
  }
  
})


// frappe.ui.form.on('Student Guardian', {
//   guardians_add: function (frm) {
//     frm.fields_dict['guardians'].grid.get_field('guardian').get_query =
//       function (doc) {
//         let guardian_list = []
//         if (!doc.__islocal) guardian_list.push(doc.guardian)
//         $.each(doc.guardians, function (idx, val) {
//           if (val.guardian) guardian_list.push(val.guardian)
//         })
//         return { filters: [['Guardian', 'name', 'not in', guardian_list]] }
//       }
//   },
// })



function calculate_age(frm) {
  const dob = frm.doc.date_of_birth;
  if (dob) {
      const birthDate = new Date(dob);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const m = today.getMonth() - birthDate.getMonth();

      if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
          age--;
      }

      frm.set_value('age', age);
  }
}

// 🔹 Get and set guardians from student_applicant
function set_guardians_from_applicant(frm) {
  fetch_guardians_for_applicant(frm.doc.student_applicant).then(guardians => {
    if (guardians.length) {
      set_guardians_in_child_table(frm, guardians);
    } else {
      frappe.show_alert({ message: __('No guardians found for this applicant'), indicator: 'orange' });
    }
  });
}

// 🔹 Fetch guardians related to student_applicant
function fetch_guardians_for_applicant(student_applicant) {
  return new Promise((resolve, reject) => {
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "Guardian",
        filters: {
          student_applicant: student_applicant 
        },
        fields: ["name", "guardian_name", "mobile_number", "relation_with_child"]
      },
      callback: function (r) {
        resolve(r.message || []);
      },
      error: function (err) {
        reject(err);
      }
    });
  });
}

// 🔹 Set guardians into the guardians child table
function set_guardians_in_child_table(frm, guardians) {
  frm.clear_table("guardians");
  guardians.forEach(guardian => {
    let row = frm.add_child("guardians");
    row.guardian = guardian.name;
    if (guardian.guardian_name) {
      row.guardian_name = guardian.guardian_name;
      row.mobile_number = guardian.mobile_number;
      row.relation_with_child = guardian.relation_with_child;
    }
  });
  frm.refresh_field("guardians");
}




