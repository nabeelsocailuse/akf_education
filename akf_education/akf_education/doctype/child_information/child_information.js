frappe.ui.form.on("Child Information", {
    refresh: function(frm) {
        calculate_hygiene_scores(frm);
    },
    hair: function(frm) {
        calculate_hygiene_scores(frm);
    },
    clothing: function(frm) {
        calculate_hygiene_scores(frm);
    },
    ears: function(frm) {
        calculate_hygiene_scores(frm);
    },
    nail: function(frm) {
        calculate_hygiene_scores(frm);
    },
    skin: function(frm) {
        calculate_hygiene_scores(frm);
    },
    eyes: function(frm) {
        calculate_hygiene_scores(frm);
    }
});

function calculate_hygiene_scores(frm) {
    let hygiene_score = 0;
    let hygiene_score2 = 0;

    if (frm.doc.hair == "Cleaned/Combed:1") {
        hygiene_score += 1;
    }
    if (frm.doc.clothing == "Cleaned:1") {
        hygiene_score += 1;
    }
    if (frm.doc.ears == "Pinna/Clean:1" || frm.doc.ears == "wax:1") {
        hygiene_score += 1;
    }

    if (frm.doc.nail == "Cleaned/cut:1") {
        hygiene_score2 += 1;
    }
    if (frm.doc.skin == "Healthy/shinning:1") {
        hygiene_score2 += 1;
    }
    if (frm.doc.eyes == "Clean:1") {
        hygiene_score2 += 1;
    }

    frm.set_value("hygiene_score", hygiene_score);
    frm.set_value("hygiene_score2", hygiene_score2);
}
