// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sponsorship", {
	refresh(frm) {
        // if (frm.doc.student_applicant) {
        //     frappe.db.get_value('Student', { student_applicant: frm.doc.student_applicant }, 'name')
        //         .then(r => frm.set_value('student_id', r.message?.name || ''));
        // }  
	},


    tenure_period(frm) {  
        let sponsorship_tenure = frm.doc.sponsorship_tenure;
        let tenure_period = frm.doc.tenure_period;
        
        if (!sponsorship_tenure || !tenure_period) {
            frappe.msgprint(__('Please select both Sponsorship Tenure and Tenure Period.'));
            return;
        }


        // Get today's date as Start Date
        let today = frappe.datetime.get_today();
        let end_date = calculateEndDate(today, sponsorship_tenure, tenure_period);

        // Set the calculated values in the form
        frm.set_value("start_date", today);
        frm.set_value("end_date", end_date);
    },


});

// Function to calculate end date
function calculateEndDate(start_date, sponsorship_tenure, tenure_period) {
    let monthsToAdd = 0;

    if (sponsorship_tenure === "Monthly") {
        monthsToAdd = 1;
    } else if (sponsorship_tenure === "Quartly") {
        monthsToAdd = 3;
    } else if (sponsorship_tenure === "Yearly") {
        monthsToAdd = 12;
    }
    // Multiply by selected tenure_period 
    let totalMonths = monthsToAdd * tenure_period; 
   
    // Calculate end date
    return frappe.datetime.add_months(start_date, totalMonths); 
}









