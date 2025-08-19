frappe.router.on("change", () => {
    let route = frappe.get_route();

    if (route[0] === "Workspaces" && route[1] === "Open Executive Dashboard") {
        frappe.set_route("executive-dashboard");
    }

    if (route[0] === "Workspaces" && route[1] === "Open Aghosh Dashboard") {
        frappe.set_route("aghosh-home-details");
    }
});

