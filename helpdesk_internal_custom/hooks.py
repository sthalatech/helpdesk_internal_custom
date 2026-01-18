app_name = "helpdesk_internal_custom"
app_title = "Helpdesk Internal Custom"
app_publisher = "Sthalatech"
app_description = "Custom app for internal departmental helpdesk with team-based permissions"
app_email = "hello@sthalatech.com"
app_license = "AGPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/helpdesk_internal_custom/css/helpdesk_internal_custom.css"
# app_include_js = "/assets/helpdesk_internal_custom/js/helpdesk_internal_custom.js"

# include js, css files in header of web template
# web_include_css = "/assets/helpdesk_internal_custom/css/helpdesk_internal_custom.css"
# web_include_js = "/assets/helpdesk_internal_custom/js/helpdesk_internal_custom.js"

# include custom scss in every website theme (without signing in)
# website_theme_scss = "helpdesk_internal_custom/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# Installation
# ------------

after_install = "helpdesk_internal_custom.install.after_install"
# after_uninstall = "helpdesk_internal_custom.uninstall.after_uninstall"

# Fixtures
# --------

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Helpdesk Internal Custom"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Helpdesk Internal Custom"]]},
]

# Override DocType methods
override_doctype_class = {
    # "HD Ticket": "helpdesk_internal_custom.overrides.ticket.CustomTicket",
}

# Permission query methods
permission_query_conditions = {
    # "HD Ticket": "helpdesk_internal_custom.permissions.get_permission_query_conditions"
}

has_permission = {
    # "HD Ticket": "helpdesk_internal_custom.permissions.has_permission"
}

# Document event hooks
doc_events = {
    # "HD Ticket": {
    #     "before_insert": "helpdesk_internal_custom.overrides.ticket.before_insert",
    #     "before_save": "helpdesk_internal_custom.overrides.ticket.before_save",
    #     "validate": "helpdesk_internal_custom.overrides.ticket.validate"
    # }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"helpdesk_internal_custom.tasks.all"
# 	],
# 	"daily": [
# 		"helpdesk_internal_custom.tasks.daily"
# 	],
# 	"hourly": [
# 		"helpdesk_internal_custom.tasks.hourly"
# 	],
# 	"weekly": [
# 		"helpdesk_internal_custom.tasks.weekly"
# 	],
# 	"monthly": [
# 		"helpdesk_internal_custom.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "helpdesk_internal_custom.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "helpdesk_internal_custom.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "helpdesk_internal_custom.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
