# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from frappe.utils.csvutils import getlink

import education.education
from education.education.api import get_assessment_details, get_grade


class AssessmentResult(Document):
	def validate(self):
		self.set_percentage()
		self.set_totals()
		# education.education.validate_student_belongs_to_group(
		# 	self.student, self.student_group
		# )
		# self.validate_maximum_score()
		# self.validate_grade()
		self.validate_duplicate()

	def set_percentage(self):
		for row in self.details:
			if(row.score and row.maximum_score):
				if row.score > row.maximum_score:
					frappe.throw(_(f"Total Marks cannot be greater than Obtained Marks, Row: {row.idx}"))
				row.percentage= (row.score / row.maximum_score) * 100
	
	def set_totals(self):
		if self.details:
			total_marks = 0.0
			obtained_marks = 0.0
			for row in self.details:
				total_marks+= row.maximum_score
				obtained_marks+= row.score
			self.total_marks = total_marks
			self.total_obtained_marks = obtained_marks

			self.total_percentage = (self.total_obtained_marks / self.total_marks) * 100


	def validate_maximum_score(self):
		assessment_details = get_assessment_details(self.assessment_plan)
		max_scores = {}
		for d in assessment_details:
			max_scores.update({d.assessment_criteria: d.maximum_score})

		for d in self.details:
			d.maximum_score = max_scores.get(d.assessment_criteria)
			if d.score > d.maximum_score:
				frappe.throw(_("Score cannot be greater than Maximum Score"))

	def validate_grade(self):
		self.total_score = 0.0
		for d in self.details:
			d.grade = get_grade(self.grading_scale, (flt(d.score) / d.maximum_score) * 100)
			self.total_score += d.score
		self.grade = get_grade(
			self.grading_scale, (self.total_score / self.maximum_score) * 100
		)

	def validate_duplicate(self):
		assessment_result = frappe.get_list(
			"Assessment Result",
			filters={
				"name": ("not in", [self.name]),
				"student": self.student,
				"academic_year": self.academic_year,
				"docstatus": ("!=", 2),
				"select_term": "Final Term",
			},
		)
		if assessment_result:
			frappe.throw(
				_("Assessment Result record {0} already exists.").format(
					getlink("Assessment Result", assessment_result[0].name)
				)
			)
		# assessment_result = frappe.get_list(
		# 	"Assessment Result",
		# 	filters={
		# 		"name": ("not in", [self.name]),
		# 		"student": self.student,
		# 		"assessment_plan": self.assessment_plan,
		# 		"docstatus": ("!=", 2),
		# 	},
		# )
		# if assessment_result:
		# 	frappe.throw(
		# 		_("Assessment Result record {0} already exists.").format(
		# 			getlink("Assessment Result", assessment_result[0].name)
		# 		)
		# 	)
