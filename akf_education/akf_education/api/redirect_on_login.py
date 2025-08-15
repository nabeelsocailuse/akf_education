# import frappe

# def redirect_on_login(login_manager):
#     # frappe.throw(f"hitting login")
#     user = frappe.get_doc("User", login_manager.user)
#     roles = [d.role for d in user.roles]

#     # Change 'Sales User' to your role and '/app/sales-invoice' to your target page
#     if "Manager Aghosh Homes" in roles:
#         frappe.throw(f"hitting login")
#         frappe.local.response["type"] = "redirect"
#         frappe.local.response["location"] = "/app/executive-dashboard"


# import frappe
# from frappe.auth import LoginManager
# from frappe import _

# @frappe.whitelist(allow_guest=True)
# def custom_login():
#     # This replicates frappe's default login
#     form_dict = frappe.local.form_dict
#     login_manager = LoginManager()

#     # Authenticate
#     login_manager.authenticate(form_dict.get("usr"), form_dict.get("pwd"))
#     login_manager.post_login()

#     # Get roles for logged-in user
#     user = frappe.get_doc("User", login_manager.user)
#     roles = [d.role for d in user.roles]

#     # Redirect based on role
#     if "Manager Aghosh Homes" in roles:
#         frappe.local.response["type"] = "redirect"
#         frappe.local.response["location"] = "/app/executive-dashboard"
#     else:
#         # Default desk
#         frappe.local.response["type"] = "redirect"
#         frappe.local.response["location"] = "/app"

#     return frappe.local.response


# import frappe
# from werkzeug.utils import redirect

# def redirect_on_login(login_manager):
#     user = frappe.get_doc("User", login_manager.user)
#     roles = [d.role for d in user.roles]

#     # Only redirect Desk users (not Portal / API logins)
#     if frappe.local.request.path == "/login" and "Manager Aghosh Homes" in roles:
#         frappe.local.flags.redirect_location = "/app/executive-dashboard"
#         raise frappe.Redirect
