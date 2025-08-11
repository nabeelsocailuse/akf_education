# Copyright (c) 2025, Mubarrim Iqbal and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Sponsorship(Document):
    def before_save(self):
        self.calculate_total_amount()
    
    def on_submit(self):
        self.create_donation_entry()

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


    # donation_entry.fund_class_id = self.fund_class_id
    # donation_entry.intention = self.intention
    # donation_entry.donor_id = self.donor_id
    # donation_entry.donation_amount = self.sponsored_amount
    # donation_entry.due_date = self.end_date
    def create_donation_entry(self):
        if not self.fund_class_id:
            frappe.throw("Fund Class ID is required to create a donation entry.")
        if not self.branch:
            frappe.throw("Branch is required to create a donation entry.")
        if not self.intention:
            frappe.throw("Intention is required to create a donation entry.")
        if not self.sponsorship_tenure:
            frappe.throw("Sponsorship Tenure is required to create a donation entry.")
        if not self.tenure_period:
            frappe.throw("Tenure Period is required to create a donation entry.")        
        if not self.sponsored_amount:
            frappe.throw("Sponsored Amount is required to create a donation entry.")
        
        donation_entry = frappe.new_doc("Donation")
        donation_entry.donor_identity = 'Known'
        donation_entry.contribution_type = 'Pledge'
        donation_entry.currency = 'PKR'
        donation_entry.company = self.company
        donation_entry.donation_cost_center = self.branch
        donation_entry.append("payment_detail", {
        "fund_class_id": self.fund_class_id,
        "donation_type": self.intention,
        "donor_id": self.donor_id,
        "donation_amount": self.sponsored_amount,
        "due_date": self.end_date
        })

        donation_entry.insert()

	
