// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Program Enrollment', {
    onload: function (frm) {
        // Set queries for academic_term based on academic_year
        frm.set_query('academic_term', function () {
            return {
                filters: {
                    academic_year: frm.doc.academic_year,
                },
            };
        });

        frm.set_query('academic_term', 'fees', function () {
            return {
                filters: {
                    academic_year: frm.doc.academic_year,
                },
            };
        });

        frm.set_query('internal_school', function () {
            return {
                filters: {
                    "aghosh_home_id": frm.doc.aghosh_home_id,
                    "type": "School"
                }
            };
        });

        // Set query for fee_schedule in fees child table
        frm.fields_dict['fees'].grid.get_field('fee_schedule').get_query = function (doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                filters: { academic_term: d.academic_term },
            };
        };

        // Set query for course based on program selection
        //   if (frm.doc.program) {
        //       frm.set_query('course', 'courses', function () {
        //           return {
        //               query: 'education.education.doctype.program_enrollment.program_enrollment.get_program_courses',
        //               filters: {
        //                   program: frm.doc.program,
        //               },
        //           };
        //       });
        //   }

        // Fetch Fee Schedules when form loads (if program & academic_year exist)
        if (frm.doc.program && frm.doc.academic_year && frm.doc.aghosh_home) {
            //   fetch_fee_schedules(frm);
            fetch_fee_components(frm);
            setTimeout(() => {
                frm.save();
            }, 250);
        }

    },

    refresh: function (frm) {
        // frm.add_custom_button(__('Create Assessment Plan'), function() {
        //     create_assessment_plan(frm);
        // }, __("Assessment Plan"));
    },

    // program: function (frm) {
    //       fetch_fee_schedules(frm);
    //       fetch_fee_components(frm);
    //       frm.events.set_course_query(frm);
    //   },
    // aghosh_home: function (frm) {
    //     fetch_fee_components(frm);
    //     frm.events.set_course_query(frm);
    // },
    // external1: function (frm) {  
    //     fetch_fee_components(frm);
    //     frm.events.set_course_query(frm);
    // },
    // school_type: function (frm) {  
    //     fetch_fee_components(frm);
    // },

    student_category: function (frm) {
        frappe.ui.form.trigger('Program Enrollment', 'program');
    },

    get_courses: function (frm) {
        frm.program_courses = [];
        frm.set_value('courses', []);

        frappe.call({
            method: 'get_courses',
            doc: frm.doc,
            callback: function (r) {
                if (r.message) {
                    frm.program_courses = r.message;
                    frm.set_value('courses', r.message);
                }
            },
        });
    },

    set_course_query: function (frm) {
        if (frm.doc.program) {
            frm.set_query('course', 'courses', function () {
                return {
                    query: 'akf_education.akf_education.doctype.program_enrollment.program_enrollment.get_program_courses',
                    filters: {
                        program: frm.doc.program,
                    },
                };
            });
        }
    }
});

function create_assessment_plan(frm) {
    frappe.call({
        method: "akf_education.akf_education.doctype.program_enrollment.program_enrollment.create_assessment_plan",
        args: {
            program: frm.doc.program,
            academic_year: frm.doc.academic_year,
            academic_term: frm.doc.academic_term,
            grading_scale: frm.doc.grading_scale
        },
        callback: function (r) {
            if (!r.exc) {
                frappe.msgprint("Assessment Plan created successfully: " + r.message);
                frm.reload_doc();
            }
        }
    });
}



// Fetch Fee Schedules and Populate Fees Table
function fetch_fee_schedules(frm) {
    if (frm.doc.program && frm.doc.academic_year) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Fee Schedule",
                filters: {
                    program: frm.doc.program,
                    academic_year: frm.doc.academic_year,
                    docstatus: 1
                },
                fields: ["academic_term", "name"]
            },
            callback: function (response) {
                if (response.message) {
                    frm.clear_table("fees");
                    response.message.forEach(fee => {
                        let row = frm.add_child("fees");
                        row.academic_term = fee.academic_term;
                        row.fee_schedule = fee.name;
                    });
                    frm.refresh_field("fees");
                }
            }
        });
    }
}


// Fetch Fee Structure Components and Populate Components Table
// function fetch_fee_components(frm) {
//     if (!frm.doc.program || !frm.doc.aghosh_home) {
//         frappe.msgprint(__('Please select both Program and Aghosh Home before fetching Fee Components.'));
//         return;
//     }

//     frappe.call({
//         method: "education.education.doctype.program_enrollment.program_enrollment.get_fee_structure_components",
//         args: { program: frm.doc.program,
//             aghosh_home: frm.doc.aghosh_home
//          },
//         callback: ({ message }) => {
//             if (!message?.length) return;

//             frm.clear_table("components");
//             message.forEach(row => frm.add_child("components", row));
//             frm.refresh_field("components");
//         }
//     });
// }




// This is commented
// function fetch_fee_components(frm) {
//     if (!frm.doc.program || !frm.doc.school_type) return;

//     frappe.call({
//         method: "akf_education.akf_education.doctype.program_enrollment.program_enrollment.get_fee_structure_components",
//         args: { 
//             program: frm.doc.program,
//             aghosh_home: frm.doc.aghosh_home || null,
//             external1: frm.doc.external1 || null,
//             school_type: frm.doc.school_type // Internal or External
//         },
//         callback: ({ message }) => {
//             frm.clear_table("components");

//             if (message?.length) {
//                 message.forEach(row => frm.add_child("components", row));
//             } else {
//                 frappe.msgprint(__('No fee structure components found for the selected filters.'));
//             }

//             frm.refresh_field("components");   
//         }
//     });
// }




// Course Filtering in Child Table
frappe.ui.form.on('Program Enrollment Course', {
    courses_add: function (frm) {
        frm.fields_dict['courses'].grid.get_field('course').get_query = function (doc) {
            var course_list = [];
            if (!doc.__islocal) course_list.push(doc.name);
            $.each(doc.courses, function (_idx, val) {
                if (val.course) course_list.push(val.course);
            });
            return {
                filters: [
                    ['Course', 'name', 'not in', course_list],
                    ['Course', 'name', 'in', frm.program_courses.map(e => e.course)],
                ],
            };
        };
    }
});























