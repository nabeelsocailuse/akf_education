frappe.router.on("change", () => {
    let route = frappe.get_route();
    // let roles = (frappe.boot && frappe.boot.user && frappe.boot.user.roles) ? frappe.boot.user.roles : [];

    console.log("Showing before if condition");
    console.log("Current route:", route);
    // console.log("User roles:", roles);


    // 2. Check both: user has the Central Office Focal Person role AND clicked Aghosh Homes workspace
    if (route[0] === "Workspaces" && route[1] === "Open Executive Dashboard") {
        console.log("Redirecting Central Office Focal Person to executive-dashboard");
        frappe.set_route("executive-dashboard");
    }

    if (route[0] === "Workspaces" && route[1] === "Open Aghosh Dashboard") {
        console.log("Redirecting Manager Aghosh Homes to Aghosh Home Details Dashboard");
        frappe.set_route("aghosh-home-details");
    }
});

