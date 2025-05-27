# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

from frappe import _


def get_data():
	return {
		"reports": [
			{
				"label": _("Reports"),
				"items": ["Final Assessment Grades", "Course wise Assessment Report"],
			}
		]
	}
