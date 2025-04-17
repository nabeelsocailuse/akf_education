frappe.pages['order-management'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Order Management',
        single_column: true
    });

    frappe.call({
        method: 'akf_education.akf_education.page.order_management.order_management.get_order_stats',
        callback: function(r) {
            if (r.message) {
                const data = r.message;
                const html = frappe.render_template("order_management", data);
                $(html).appendTo(page.body);
                setTimeout(() => {
                    if ($('#example').length) {
                        $('#example').DataTable({
                            pageLength: 10
                        });
                    } else {
                        console.error("Table with ID #example not found.");
                    }
                }, 100);
            }
        }
    });
};
