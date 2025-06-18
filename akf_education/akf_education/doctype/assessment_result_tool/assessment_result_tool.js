// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt


frappe.ui.form.on('Assessment Result Tool', {
	setup: function (frm) {
		// frm.add_fetch("assessment_plan", "student_group", "student_group");
	},

	refresh: function (frm) {
		frm.set_query("student_id", function () {
			return {
				filters: {
					status: "Active"
				},
			};
		});
		// if (frappe.route_options) {
		// 	frm.set_value("student_group", frappe.route_options.student_group);
		// 	frm.set_value("assessment_plan", frappe.route_options.assessment_plan);
		// 	frappe.route_options = null;
		// } else {
		// 	frm.trigger("assessment_plan");
		// }
		frm.disable_save();
		frm.page.clear_indicator();
	},

	get_subjects: function (frm) {
		frm.set_value('details', []);
		// frm.set_value('sponsors', []);
		frappe.call({
			method: 'get_courses',
			doc: frm.doc,
			callback: function (r) {
				console.log(r.message);
				if (r.message) {
					r.message.forEach(course => {
						let row = frm.add_child("details");
						row.subject = course.course;
					});
					frm.refresh_field("details");
					//   frm.set_value('students', r.message)
				}
			},
		});
	},

	student_id: function (frm) {
		if (frm.doc.student_id) {
			frappe.call({
				method: 'get_latest_checked_enrollment',
				doc: frm.doc,
				callback: function (r) {
					console.log(r.message[0]);
					frm.set_value("current_program_enrollment", null);
					frm.set_value("program", null);
					frm.set_value("academic_year", null);
					if (r.message[0]) {
						frm.set_value("current_program_enrollment", r.message[0].name);
						frm.set_value("program", r.message[0].program);
						frm.set_value("academic_year", r.message[0].academic_year);
					} else {
						frappe.msgprint("No Program Enrollment found for this student.");
					}
				}
			});
		}
	},

	generate_result: function (frm) {
		if (frm.doc.details && frm.doc.details.length > 0) {
			frappe.call({
				method: 'generate_assessment_result',
				doc: frm.doc,
				callback: function (r) {
					// console.log(r.message[0]);
					frm.set_value("student_id", null);
					frm.set_value("current_program_enrollment", null);
					frm.set_value("program", null);
					frm.set_value("academic_year", null);
					frm.set_value("details", []);
					frappe.msgprint("Assessment results generated successfully.");
				}
			});
		}
	},
	// assessment_plan: function(frm) {
	// 	frm.doc.show_submit = false;
	// 	if(frm.doc.assessment_plan) {
	// 		if (!frm.doc.student_group)
	// 			return
	// 		frappe.call({
	// 			method: "education.education.api.get_assessment_students",
	// 			args: {
	// 				"assessment_plan": frm.doc.assessment_plan,
	// 				"student_group": frm.doc.student_group
	// 			},
	// 			callback: function(r) {
	// 				if (r.message) {
	// 					frm.doc.students = r.message;
	// 					frm.events.render_table(frm);
	// 					for (let value of r.message) {
	// 						if (!value.docstatus) {
	// 							frm.doc.show_submit = true;
	// 							break;
	// 						}
	// 					}
	// 					frm.events.submit_result(frm);
	// 				}
	// 			}
	// 		});
	// 	}
	// },

	// render_table: function(frm) {
	// 	$(frm.fields_dict.result_html.wrapper).empty();
	// 	let assessment_plan = frm.doc.assessment_plan;
	// 	frappe.call({
	// 		method: "education.education.api.get_assessment_details",
	// 		args: {
	// 			assessment_plan: assessment_plan
	// 		},
	// 		callback: function(r) {
	// 			frm.events.get_marks(frm, r.message);
	// 		}
	// 	});
	// },

	// get_marks: function(frm, criteria_list) {
	// 	let max_total_score = 0;
	// 	criteria_list.forEach(function(c) {
	// 		max_total_score += c.maximum_score
	// 	});
	// 	var result_table = $(frappe.render_template('assessment_result_tool', {
	// 		frm: frm,
	// 		students: frm.doc.students,
	// 		criteria: criteria_list,
	// 		max_total_score: max_total_score
	// 	}));
	// 	result_table.appendTo(frm.fields_dict.result_html.wrapper);

	// 	result_table.on('change', 'input', function(e) {
	// 		let $input = $(e.target);
	// 		let student = $input.data().student;
	// 		let max_score = $input.data().maxScore;
	// 		let value = $input.val();
	// 		if(value < 0) {
	// 			$input.val(0);
	// 		} else if(value > max_score) {
	// 			$input.val(max_score);
	// 		}
	// 		let total_score = 0;
	// 		let student_scores = {};
	// 		student_scores["assessment_details"] = {}
	// 		result_table.find(`input[data-student=${student}].student-result-data`)
	// 			.each(function(el, input) {
	// 				let $input = $(input);
	// 				let criteria = $input.data().criteria;
	// 				let value = parseFloat($input.val());
	// 				if (!Number.isNaN(value)) {
	// 					student_scores["assessment_details"][criteria] = value;
	// 				}
	// 				total_score += value;
	// 		});
	// 		if(!Number.isNaN(total_score)) {
	// 			result_table.find(`span[data-student=${student}].total-score`).html(total_score);
	// 		}
	// 		if (Object.keys(student_scores["assessment_details"]).length === criteria_list.length) {
	// 			student_scores["student"] = student;
	// 			student_scores["total_score"] = total_score;
	// 			result_table.find(`[data-student=${student}].result-comment`)
	// 				.each(function(el, input){
	// 				student_scores["comment"] = $(input).val();
	// 			});
	// 			frappe.call({
	// 				method: "education.education.api.mark_assessment_result",
	// 				args: {
	// 					"assessment_plan": frm.doc.assessment_plan,
	// 					"scores": student_scores
	// 				},
	// 				callback: function(r) {
	// 					let assessment_result = r.message;
	// 					if (!frm.doc.show_submit) {
	// 						frm.doc.show_submit = true;
	// 						frm.events.submit_result;
	// 					}
	// 					for (var criteria of Object.keys(assessment_result.details)) {
	// 						result_table.find(`[data-criteria=${criteria}][data-student=${assessment_result
	// 							.student}].student-result-grade`).each(function(e1, input) {
	// 								$(input).html(assessment_result.details[criteria]);
	// 						});
	// 					}
	// 					result_table.find(`span[data-student=${assessment_result.student}].total-score-grade`).html(assessment_result.grade);
	// 					let link_span = result_table.find(`span[data-student=${assessment_result.student}].total-result-link`);
	// 					$(link_span).css("display", "block");
	// 					$(link_span).find("a").attr("href", "/app/assessment-result/"+assessment_result.name);
	// 				}
	// 			});
	// 		}
	// 	});
	// },

	// submit_result: function(frm) {
	// 	if (frm.doc.show_submit) {
	// 		frm.page.set_primary_action(__("Submit"), function() {
	// 			frappe.call({
	// 				method: "education.education.api.submit_assessment_results",
	// 				args: {
	// 					"assessment_plan": frm.doc.assessment_plan,
	// 					"student_group": frm.doc.student_group
	// 				},
	// 				callback: function(r) {
	// 					if (r.message) {
	// 						frappe.msgprint(__("{0} Result submittted", [r.message]));
	// 					} else {
	// 						frappe.msgprint(__("No Result to submit"));
	// 					}
	// 					frm.events.assessment_plan(frm);
	// 				}
	// 			});
	// 		});
	// 	}
	// 	else {
	// 		frm.page.clear_primary_action();
	// 	}
	// }
});