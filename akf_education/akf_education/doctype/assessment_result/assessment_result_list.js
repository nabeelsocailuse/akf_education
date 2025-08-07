// frappe.listview_settings['Assessment Result'] = {
//     onload: function(listview) {
//         listview.page.add_inner_button('Download Multiple PDFs', () => {
//             const selected = listview.get_checked_items().map(row => row.name);
//             if (!selected.length) {
//                 frappe.msgprint('Please select at least one record.');
//                 return;
//             }

//             frappe.call({
//                 method: 'akf_education.akf_education.api.multiple_pdfs.download_multiple_pdfs',
//                 args: {
//                     doctype: 'Assessment Result',
//                     docnames: JSON.stringify(selected),
//                     print_format: 'Student Progress Report'
//                 },
//                 callback: function(r) {
//                     if (r.message.file_url) {
//                         window.open(r.message.file_url);
//                     }
//                 }
//             });
//         });
//     }
// }

frappe.listview_settings['Assessment Result'] = {
    onload: function (listview) {
        listview.page.add_inner_button('Download Multiple PDFs', () => {
            const selected = listview.get_checked_items().map(row => row.name);
            if (!selected.length) {
                frappe.msgprint('Please select at least one record.');
                return;
            }

            // Show dialog to select print format
            frappe.db.get_list('Print Format', {
                filters: { doc_type: 'Assessment Result' },
                fields: ['name']
            }).then(printFormats => {
                let options = printFormats.map(pf => pf.name);

                let d = new frappe.ui.Dialog({
                    title: 'Select Print Format',
                    fields: [
                        {
                            label: 'Print Format',
                            fieldname: 'print_format',
                            fieldtype: 'Select',
                            options: options,
                            reqd: 1
                        }
                    ],
                    primary_action_label: 'Download',
                    primary_action(values) {
                        d.hide();

                        frappe.call({
                            method: 'akf_education.akf_education.api.multiple_pdfs.download_multiple_pdfs',
                            args: {
                                doctype: 'Assessment Result',
                                docnames: JSON.stringify(selected),
                                print_format: values.print_format
                            },
                            callback: function (r) {
                                if (r.message.file_url) {
                                    window.open(r.message.file_url);
                                }
                            }
                        });
                    }
                });

                d.show();
            });
        });
    }
}
