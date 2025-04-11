# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Sponsorship(Document):
    def before_save(self):
        self.set_student_id()
        
    def set_student_id(self):
        if self.student_applicant:
            student = frappe.db.get_value('Student', {'student_applicant': self.student_applicant}, 'name')
            self.student_id = student or ''

		           

    
    

	
