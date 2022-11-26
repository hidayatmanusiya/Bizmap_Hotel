import frappe
import requests
import json
import requests
from requests.structures import CaseInsensitiveDict


@frappe.whitelist(allow_guest=True)
def insertbooking():
	company = frappe.defaults.get_user_default("Company")
	abbr = frappe.db.get_value("Company", company, 'abbr')

	url = "https://kiviosandbox.staah.net/SUAPI/jservice/Reservation"

	headers = CaseInsensitiveDict()
	headers["Authorization"] = "Basic bzZVZndCVW86bnN5S05nZ1Y"
	headers["Content-Type"] = "application/json"

	data = {
		# "hotelid": "SP-1011"
		# "hotelid": "SB-101"
		"hotelid": "KC"

	}

	response = requests.post(url, headers=headers, data=json.dumps(data))
	if (response.status_code == 200):
		response = response.json()
		for i in response['reservations']:
			if i['status'] == "new":
				no_of_rooms = len(i['rooms'])
			guests = 0
			for room in i['rooms']:
				children = room['numberofchildren']
				adults = room['numberofadults']
				no_of_guest = int(children or 0) + int(adults or 0)
				guests += no_of_guest
			for room in i['rooms']:
				for price in room['price']:
					for addon in room['addons']:
						# Create Customer
						customer_list = frappe.get_list('Customer', fields=['customer_name'])
						check = {'customer_name': room['guest_name']}
						if check not in customer_list:
							create_customer(room['guest_name'])

						# Create Contact
						contact_list = frappe.get_list('Contact', fields=['first_name'])
						check = {'first_name': room['guest_name']}
						if check not in contact_list:
							create_contact(room['guest_name'], i['customer']['email'], i['customer']['telephone'])

						transactionid = i['id']
						nights = addon['nights']
						qty = no_of_rooms * int(nights)

						# Create Sales Order
						sales_orders = frappe.get_list('Sales Order', fields=['transactionid'])
						check = {'transactionid': i['id']}
						if check not in sales_orders:
							param = {
										"company": company, "transactionid": transactionid, "guest_name": room['guest_name'],
										"no_of_guest": guests, "arrival_date": room['arrival_date'], "no_of_rooms": no_of_rooms,
										"nights": nights, "departure_date": room['departure_date'], "mealplan": price['mealplan'],
										"id": room['id'], "totalbeforetax": room['totalbeforetax'], "qty": qty, "abbr": abbr,
										"totaltax": room['totaltax']
									}
							create_sales_order(param)
							# frappe.msgprint("Data Inserted Successfully")

	else:
		frappe.msgprint("Invalid Request!")


def create_customer(guest_name):
	customer = frappe.get_doc({
		"doctype": "Customer",
		"customer_name": guest_name,
		"customer_group": 'Individual',
		"territory": 'India'
	})
	customer.save()


def create_contact(guest_name, email, telephone):
	guest = frappe.get_doc({
			"doctype": "Contact",
		 			"first_name": guest_name,
		 			"gender": "Male"
	})
	guest.append("email_ids", {
		'email_id': email,
		'is_primary': 1,
	})
	guest.append("phone_nos", {
		'phone': telephone,
		'is_primary_mobile_no': 1,
	})
	guest.append("links", {
		'link_doctype': 'Customer',
		'link_name': guest_name,
		'link_title': guest_name,
	})

	guest.save()


def create_sales_order(param):
	sales_order_api = frappe.get_doc({
			"doctype": "Sales Order",
			"company": param["company"],
			"customer": param["guest_name"],
			"guest_cf": param["guest_name"]+"-"+param["guest_name"],
			"booking_type": "Online Booking",
			"transactionid": param["transactionid"],
			"check_in_cf": param["arrival_date"],
			"no_of_nights_cf": param["nights"],
			"check_out_cf": param["departure_date"],
			"no_of_guest_cf": param["no_of_guest"],
			"room_type_cf": param["id"],
			"room_package_cf": param["mealplan"],
			"number_of_room": param["no_of_rooms"],
			"room_rate_cf": param["totalbeforetax"],
	})

	sales_order_api.append("items", {
		'item_code': param["mealplan"],
		'item_name': param["mealplan"],
		'qty': param["qty"],
		"reservation_date_from": param["arrival_date"],
		"reservation_date_to": param["departure_date"],
		"rate": param["totalbeforetax"],

	})

	sales_order_api.append("taxes", {
		'charge_type': "Actual",
		'account_head': "TAX 18% - " + param["abbr"],
		'rate': "0.00",
		'tax_amount': param["totaltax"],
		'description': "TAX 18% - " + param["abbr"],
	})

	sales_order_api.save()
	sales_order_api.submit()
