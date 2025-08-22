import frappe

@frappe.whitelist()
def reroute():
    user = frappe.session.user
    roles = frappe.get_roles(user)

    frappe.local.response["home_page"] = "/app/self-service"
    
    if "Central Office Focal Person" in roles:
        frappe.local.response["home_page"] = "/app/executive-dashboard"
        return
    elif "Manager Aghosh Homes" in roles:
        frappe.local.response["home_page"] = "/app/aghosh-home-details"
        return 
    elif "Aghosh Administrator" in roles:
        frappe.local.response["home_page"] = "/app/aghosh-home-details"
        return