from . import __version__ as app_version

app_name = "bizmap_hotel"
app_title = "BizMap Hotel"
app_publisher = "BizMap"
app_description = "BizMap Hotel"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "rajat.singh@bizmap.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bizmap_hotel/css/bizmap_hotel.css"
# app_include_js = "/assets/bizmap_hotel/js/bizmap_hotel.js"

# include js, css files in header of web template
# web_include_css = "/assets/bizmap_hotel/css/bizmap_hotel.css"
# web_include_js = "/assets/bizmap_hotel/js/bizmap_hotel.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bizmap_hotel/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	#"doctype" : "public/js/doctype.js",
	"Sales Order": "public/js/sales_order.js",
	"Room Folio HMS": "public/js/room_folio_hms.js",
	"Sales Invoice": "public/js/sales_invoice.js",
	"Payment Entry": "public/js/payment_entry.js",
	"Sales Invoice": "public/js/sales_invoice.js",
	"Sign In Sheet HMS": "public/js/sign_in_sheet_hms.js"

}
doctype_list_js = {
	"Room Folio HMS": "public/js/room_folio_hms_list.js",
	"Sales Order": "public/js/sales_order_list.js",
	"Room Type HMS": "public/js/room_type_hms_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "bizmap_hotel.install.before_install"
# after_install = "bizmap_hotel.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bizmap_hotel.uninstall.before_uninstall"
# after_uninstall = "bizmap_hotel.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bizmap_hotel.notifications.get_notification_config"

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

doc_events = {
	"Sales Order": {
		"before_submit": "bizmap_hotel.bizmap_hotel.doctype.sales_order.before_submit",
		"on_submit": "bizmap_hotel.utill.api.create_ledger"
	},
	# "Payment Entry":{
	#   "before_submit":"bizmap_hotel.bizmap_hotel.doctype.payment_entry.before_submit"
	#},
	"Room Folio HMS": {
		"on_change": "bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.on_change",
		"on_update_after_submit": "bizmap_hotel.utill.api.create_ledger"
	},
	"Room Cleaning": {
		"before_submit": "bizmap_hotel.bizmap_hotel.doctype.room_cleaning.room_cleaning.before_submit"
	},
	"Sign In Sheet HMS": {
		"before_submit": "bizmap_hotel.bizmap_hotel.doctype.sign_in_sheet_hms.sign_in_sheet_hms.before_submit"
	},
	"Room HMS": {
		"before_insert": "bizmap_hotel.bizmap_hotel.doctype.room_hms.room_hms.validate_no_of_rooms"
	}
}

# Scheduled Tasks
# ---------------
scheduler_events = {
	"cron": {
		"* * * * *": [
					"bizmap_hotel.utill.booking.insertbooking",
					"bizmap_hotel.utill.room.update_room",
					"bizmap_hotel.utill.booking_staah.insertbooking",
					"bizmap_hotel.utill.room_staah.update_room"

		]
	}
}

# scheduler_events = {
# 	"all": [
# 		"bizmap_hotel.tasks.all"
# 	],
# 	"daily": [
# 		"bizmap_hotel.tasks.daily"
# 	],
# 	"hourly": [
# 		"bizmap_hotel.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bizmap_hotel.tasks.weekly"
# 	]
# 	"monthly": [
# 		"bizmap_hotel.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "bizmap_hotel.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "bizmap_hotel.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bizmap_hotel.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"bizmap_hotel.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
