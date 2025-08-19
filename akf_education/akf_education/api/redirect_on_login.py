import frappe

@frappe.whitelist()
def reroute():
    user = frappe.session.user
    roles = frappe.get_roles(user)
    
    if "Central Office Focal Person" in roles:
        frappe.local.response["home_page"] = "/app/executive-dashboard"
    elif "Manager Aghosh Homes" or "Aghosh Administrator" in roles:
        frappe.local.response["home_page"] = "/app/aghosh-home-details"