// Copyright (c) 2025, Mubarrim Iqbal and contributors
// For license information, please see license.txt

frappe.ui.form.on('Health Checkup', {
    refresh: function(frm) {
      frm.set_query("student_id", function () {
			return {
				filters: {
					status: "Active"
				},
			};
		});
      frm.fields_dict["prescription"].grid.get_field("drug").get_query = function (doc, cdt, cdn) {
      return {
        filters: {
          "item_group": ["in", ["Medicine", "Drug"]],
          "is_stock_item": 1,
        }
      };
    };
      calculate_hygiene_score(frm);
  
      // 2️⃣ Set up your student_id filter
      frm.set_query("student", function() {
        return {
          filters: {
            aghosh_home_id: frm.doc.aghosh_home
          }
        };
      });
    },
  
    hair:     function(frm) { calculate_hygiene_score(frm); },
    nails:    function(frm) { calculate_hygiene_score(frm); },
    clothing: function(frm) { calculate_hygiene_score(frm); },
    skin:     function(frm) { calculate_hygiene_score(frm); },
    ears:     function(frm) { calculate_hygiene_score(frm); },
    eyes:     function(frm) { calculate_hygiene_score(frm); }
  });
  

function calculate_hygiene_score(frm) {
    let score = 0;

    score += frm.doc.hair ? parseInt(frm.doc.hair.split(':')[1]) : 0;
    score += frm.doc.nails ? parseInt(frm.doc.nails.split(':')[1]) : 0;
    score += frm.doc.clothing ? parseInt(frm.doc.clothing.split(':')[1]) : 0;
    score += frm.doc.skin ? parseInt(frm.doc.skin.split(':')[1]) : 0;
    score += frm.doc.ears ? parseInt(frm.doc.ears.split(':')[1]) : 0;
    score += frm.doc.eyes ? parseInt(frm.doc.eyes.split(':')[1]) : 0;

    frm.set_value('hygiene_score1', score);
}
