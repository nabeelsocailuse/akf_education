# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Sponsorship(Document):
    def before_save(self):
        # self.set_student_id()
        self.calculate_total_amount()
        
    # def set_student_id(self):
    #     if self.student_applicant:
    #         student = frappe.db.get_value('Student', {'student_applicant': self.student_applicant}, 'name')
            # self.student_id = student or ''

    def calculate_total_amount(self):
        monthsToAdd = 1.0
        if self.sponsored_amount and self.tenure_period:
            if (self.sponsorship_tenure == "Monthly"):
                monthsToAdd = 1.0
            elif (self.sponsorship_tenure == "Quarterly"):
                monthsToAdd = 3.0
            elif (self.sponsorship_tenure == "Yearly"):
                monthsToAdd = 12.0
                
            self.total_sponsored_amount = monthsToAdd*self.sponsored_amount*self.tenure_period

    
    

	
