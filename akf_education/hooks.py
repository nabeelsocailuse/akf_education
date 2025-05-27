app_name = "akf_education"
app_title = "Akf Education"
app_publisher = "Mubarrim Iqbal"
app_description = "Aghosh Homes"
app_email = "mubarrim@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css =[
    # "/assets/akf_education/css/jquery.dataTables.min.css",
    # "/assets/akf_education/css/bootstrap-table.min.css",
    # "/assets/akf_education/css/bootstrap.min.css",
    # "/assets/akf_education/css/index.css",


]
app_include_js = [
    # "/assets/akf_education/js/highcharts-more.js",
    # "/assets/akf_education/js/solid_gauge.js",
    "/assets/akf_education/js/leaflet.js",
    "/assets/akf_education/js/leaflet.markercluster.js",
    # "/assets/akf_education/js/jquery.min.js",
    # "/assets/akf_education/js/jquery.bootstrap.min.js",
#     "/assets/akf_education/js/jquery.dataTables.min.js",
#     "/assets/akf_education/js/jquery-3.7.1.min.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/akf_education/css/akf_education.css"
# web_include_js = "/assets/akf_education/js/akf_education.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "akf_education/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "akf_education/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "akf_education.utils.jinja_methods",
# 	"filters": "akf_education.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "akf_education.install.before_install"
# after_install = "akf_education.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "akf_education.uninstall.before_uninstall"
# after_uninstall = "akf_education.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "akf_education.utils.before_app_install"
# after_app_install = "akf_education.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "akf_education.utils.before_app_uninstall"
# after_app_uninstall = "akf_education.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "akf_education.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# doc_events = {
#     "Student": {
#         "on_trash": "akf_education.akf_education.doctype.student.student.on_trash"
#     }
# }



# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "0 0 1 * *": [  # At 00:00 on day-of-month 1
            "akf_education.akf_education.api.fee_cron.generate_monthly_fees"
        ]
    }
	# "all": [
	# 	"akf_education.tasks.daily"
	# ],
	# "daily": [
	# 	"akf_education.tasks.daily"
	# ],
	# "hourly": [
	# 	"akf_education.tasks.hourly"
	# ],
	# "weekly": [
	# 	"akf_education.tasks.weekly"
	# ],
	# "monthly": [
	# 	"akf_education.tasks.monthly"
	# ],
    
}

# Testing
# -------

# before_tests = "akf_education.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "akf_education.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "akf_education.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["akf_education.utils.before_request"]
# after_request = ["akf_education.utils.after_request"]

# Job Events
# ----------
# before_job = ["akf_education.utils.before_job"]
# after_job = ["akf_education.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"akf_education.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

