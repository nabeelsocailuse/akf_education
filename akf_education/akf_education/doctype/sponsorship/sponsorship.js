// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sponsorship", {
	refresh(frm) {
            frm.set_query("student_id", function() {
                return {
                    filters: {
                        "status": "Active"
                    }
                };
            });
	},

    start_date(frm){
        let sponsorship_tenure = frm.doc.sponsorship_tenure;
        let tenure_period = frm.doc.tenure_period;
        
        if (!sponsorship_tenure || !tenure_period) {
            frappe.msgprint(__('Please select both Sponsorship Tenure and Tenure Period'));
            return;
        }
        
        let today = frm.doc.start_date;
        let end_date = calculateEndDate(today, sponsorship_tenure, tenure_period);

        frm.set_value("start_date", today);
        frm.set_value("end_date", end_date);
    },
    tenure_period(frm) {  
        let sponsorship_tenure = frm.doc.sponsorship_tenure;
        let tenure_period = frm.doc.tenure_period;
        let today = frm.doc.start_date;
        
        if (!sponsorship_tenure || !tenure_period || !today) {
            // frappe.msgprint(__('Please select both Sponsorship Tenure, Tenure Period and Start Date'));
            return;
        }

        let end_date = calculateEndDate(today, sponsorship_tenure, tenure_period);

        // Set the calculated values in the form
        frm.set_value("start_date", today);
        frm.set_value("end_date", end_date);
    },
    sponsorship_tenure(frm) {  
        let sponsorship_tenure = frm.doc.sponsorship_tenure;
        let tenure_period = frm.doc.tenure_period;
        let today = frm.doc.start_date;
        // let today = frappe.datetime.get_today();
        
        if (!sponsorship_tenure || !tenure_period || !today) {
            // frappe.msgprint(__('Please select both Sponsorship Tenure, Tenure Period and Start Date'));
            return;
        }

        
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
    } else if (sponsorship_tenure === "Quarterly") {
        monthsToAdd = 3;
    } else if (sponsorship_tenure === "Yearly") {
        monthsToAdd = 12;
    }
    // Multiply by selected tenure_period 
    let totalMonths = monthsToAdd * tenure_period; 
   
    // Calculate end date
    return frappe.datetime.add_months(start_date, totalMonths); 
}









