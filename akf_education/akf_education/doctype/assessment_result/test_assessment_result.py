# Copyright (c) 2025, Mubarrim Iqbal and Contributors
# See license.txt

import unittest

from education.education.api import get_grade

# test_records = frappe.get_test_records('Assessment Result')


class TestAssessmentResult(unittest.TestCase):
	def test_grade(self):
		grade = get_grade("_Test Grading Scale", 80)
		self.assertEqual("A", grade)

		grade = get_grade("_Test Grading Scale", 70)
		self.assertEqual("B", grade)
