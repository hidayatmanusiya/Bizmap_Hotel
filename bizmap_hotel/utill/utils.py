import frappe
from frappe.utils import getdate


def shift_room_or_upgrade_booking(room_folio, method):
	room_no = frappe.db.get_value("Room Folio HMS", room_folio.name, "room_no")
	room_type = frappe.db.get_value(
		"Room Folio HMS", room_folio.name, "room_type")
	room_package = frappe.db.get_value(
		"Room Folio HMS", room_folio.name, "room_package")

	if room_folio.room_no != room_no or room_folio.room_type != room_type or room_folio.room_package != room_package:
		if room_folio.reservation:
			update_sales_order(room_folio)
		create_room_balance_ledger(room_folio)


def update_sales_order(room_folio):
	sales_order = frappe.get_doc("Sales Order", room_folio.reservation)
	sales_order.room_type_cf = room_folio.room_type
	sales_order.room_package_cf = room_folio.room_package
	sales_order.db_update()


def create_room_balance_ledger(room_folio):
	ledger = frappe.new_doc("Room Balance Ledger")
	ledger.reference = room_folio.reservation
	ledger.folio_reference = room_folio.name
	ledger.room_type = room_folio.room_type
	ledger.room = room_folio.room_no
	ledger.from_date = getdate(room_folio.check_in)
	ledger.to_date = getdate(room_folio.check_out)
	status = ""
	if room_folio.status == "Checked In":
		status = "IN"
	elif room_folio.status == "Checked Out":
		status = "OUT"
	ledger.record_type = status
	ledger.insert()
