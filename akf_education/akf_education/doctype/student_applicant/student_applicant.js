frappe.ui.form.on('Student Applicant', {
  refresh: function (frm) {
    console.log("Sulatan Shan");
    frm.set_query('academic_term', function (doc, cdt, cdn) {
      return {
        filters: {
          academic_year: frm.doc.academic_year,
        },
      }
    });

    if (!frm.is_new() && frm.doc.application_status === 'Applied') {
      frm.add_custom_button(__('Approve'), function () {
        frm.set_value('application_status', 'Approved');
        frm.save_or_update();
      }, 'Actions');

      frm.add_custom_button(__('Reject'), function () {
        frm.set_value('application_status', 'Rejected');
        frm.save_or_update();
      }, 'Actions');
    }

    if (!frm.is_new() && frm.doc.application_status === 'Approved') {
      frm.add_custom_button(__('Enroll'), function () {
        frm.events.enroll(frm);
      });

      frm.add_custom_button(__('Reject'), function () {
        frm.set_value('application_status', 'Rejected');
        frm.save_or_update();
      }, 'Actions');
    }

    if (!frm.is_new() && frm.doc.application_status === 'Rejected') {
      frm.add_custom_button(__('Approve'), function () {
        frm.set_value('application_status', 'Approved');
        frm.save_or_update();
      }, 'Actions');
    }

    frappe.realtime.on('enroll_student_progress', function (data) {
      if (data.progress) {
        frappe.hide_msgprint(true);
        frappe.show_progress(__('Enrolling student'), data.progress[0], data.progress[1]);
      }
    });

    frappe.db.get_value('Education Settings', { name: 'Education Settings' }, 'user_creation_skip', (r) => {
      if (cint(r.user_creation_skip) !== 1) {
        frm.set_df_property('student_email_id', 'reqd', 0);
      }
    });
    frappe.call({
      method: "akf_education.akf_education.doctype.student_applicant.student_applicant.get_student_admission_program_details",
      args: {
        academic_year: frm.doc.academic_year,
        program: frm.doc.program
      },
      callback: function (r) {
        if (r.message && r.message.length) {
          console.log("Program Details:", r.message);
          minAge = r.message[0].min_age;
          maxAge = r.message[0].max_age;
        } else {
          console.log("No data found.");
        }
      }
    });
    
    
  },

  validate: function (frm) {
    showAgeMessage(frm);
  },

  enroll: function (frm) {
    frappe.model.open_mapped_doc({
      method: 'education.education.api.enroll_student',
      frm: frm,
    });
  },
});

function showAgeMessage(frm) {
  if (frm.doc.date_of_birth1) {
    const dob = new Date(frm.doc.date_of_birth1);
    const today = new Date();

    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
      age--;
    }

    console.log("Your age is:", age);
    console.log("Min Age Criteria:", minAge, "Max Age Criteria:", maxAge);

    // Validate against program age criteria if both are set
    if (minAge !== null && maxAge !== null) {
      if (age < minAge) {
        frappe.throw(`Your age is ${age} — it's less than the program's minimum age of ${minAge}.`);
      } else if (age > maxAge) {
        frappe.throw(`Your age is ${age} — it's higher than the program's maximum age of ${maxAge}.`);
      } else {
        frappe.msgprint(`You are ${age} years old and meet the program's age criteria.`);
      }
    } else {
      // fallback message if criteria not fetched yet
      frappe.msgprint(`You are ${age} years old. Program age criteria not loaded yet.`);
    }
  }
}




