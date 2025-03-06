// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on('Health Checkup', {
    refresh: function(frm) {
        calculate_hygiene_score(frm);
    },
    
    hair: function(frm) {
        calculate_hygiene_score(frm);
    },

    nails: function(frm) {
        calculate_hygiene_score(frm);
    },

    clothing: function(frm) {
        calculate_hygiene_score(frm);
    },

    skin: function(frm) {
        calculate_hygiene_score(frm);
    },

    ears: function(frm) {
        calculate_hygiene_score(frm);
    },

    eyes: function(frm) {
        calculate_hygiene_score(frm);
    }
});

function calculate_hygiene_score(frm) {
    let score = 0;

    // Fetch values from the form
    score += frm.doc.hair ? parseInt(frm.doc.hair.split(':')[1]) : 0;
    score += frm.doc.nails ? parseInt(frm.doc.nails.split(':')[1]) : 0;
    score += frm.doc.clothing ? parseInt(frm.doc.clothing.split(':')[1]) : 0;
    score += frm.doc.skin ? parseInt(frm.doc.skin.split(':')[1]) : 0;
    score += frm.doc.ears ? parseInt(frm.doc.ears.split(':')[1]) : 0;
    score += frm.doc.eyes ? parseInt(frm.doc.eyes.split(':')[1]) : 0;

    // Set the calculated value to Hygiene Score field
    frm.set_value('hygiene_score1', score);
}
