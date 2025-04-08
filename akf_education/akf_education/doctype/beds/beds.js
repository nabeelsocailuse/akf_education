// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Beds", {
	refresh(frm) {
       let  bed_number = frm.doc.bed_number
        console.log("Bed number", bed_number);
        frm.refresh_field("bed_number");

	},
});
