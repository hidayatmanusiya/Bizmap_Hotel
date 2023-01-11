import frappe


def shift_room_or_upgrade_booking(room_folio, method):
    room_no = frappe.db.get_value("Room Folio HMS", room_folio.name, "room_no")
    room_type = frappe.db.get_value("Room Folio HMS", room_folio.name, "room_type")
    room_package = frappe.db.get_value("Room Folio HMS", room_folio.name, "room_package")

    if room_folio.room_no != room_no or room_folio.room_type != room_type or room_folio.room_package != room_package:
        if room_folio.reservation:
            sales_order = frappe.get_doc("Sales Order", room_folio.reservation)
            sales_order.room_type_cf = room_folio.room_type
            sales_order.room_package_cf = room_folio.room_package
            sales_order.db_update()