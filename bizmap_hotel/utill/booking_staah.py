import frappe
import requests
import json
from datetime import date, datetime, timedelta
import requests
from requests.structures import CaseInsensitiveDict
import re


@frappe.whitelist(allow_guest=True)
def insertbooking():

    company = frappe.defaults.get_user_default("Company")
    abbr = frappe.db.sql(
        "select abbr from `tabCompany` where company_name = %s", company)
    abbr = str(abbr)
    abbr = abbr.replace("(", "")
    abbr = abbr.replace(")", "")
    abbr = abbr.replace(",", "")
    abbr = abbr.replace("'", "")
    # frappe.msgprint(abbr)

    url = "https://kiviosandbox.staah.net/SUAPI/jservice/Reservation"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Basic bzZVZndCVW86bnN5S05nZ1Y"
    headers["Content-Type"] = "application/json"

    data = {
        "hotelid": "SB-101"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if (response.status_code == 200):
        tr = response.json()
        for i in tr['reservations']:
            list_id = []
            if i['id'] not in list_id:
                list_id.append(i['id'])
                list_id = str(list_id)
                list_id = list_id.replace("[", "")
                list_id = list_id.replace("]", "")
                list_id = list_id.replace("'", "")

            if i['id'] == list_id:
                if i['status'] == "new":
                    no_of_rooms = len(i['rooms'])

            for c in i['rooms']:
                for m in c['price']:
                    for a in c['addons']:

                        # Sum Child and Adult - No Of Guest
                        child = c['numberofchildren']
                        adult = c['numberofadults']
                        no_of_guest = sum(int(d) for d in child) + sum(int(d1) for d1 in adult)

                        result_room = [r['id'] for r in tr['reservations']]
                        if len(result_room) > 0:
                            room_count = len(result_room)
                        # frappe.msgprint(room_count)

                        # Create customer
                        customer_list = frappe.get_list(
                            'Customer', fields=['customer_name'])
                        check = {'customer_name': c['guest_name']}
                        if check not in customer_list:
                            customer = frappe.get_doc({
                                "doctype": "Customer",
                                "customer_name": c['guest_name'],
                                "customer_group": 'Individual',
                                "territory": 'India'
                            })
                            customer.insert()

                        # Create contact
                        contact_list = frappe.get_list(
                            'Contact', fields=['first_name'])
                        check = {'first_name': c['guest_name']}
                        if check not in contact_list:
                            guest = frappe.get_doc({
                                "doctype": "Contact",
                                "first_name": c['guest_name'],
                                "gender": "Male"

                            })

                        # Mail
                            guest.append("email_ids", {
                                'email_id': i['customer']['email'],
                                'is_primary': 1,


                            })

                            # Mobile Number
                            guest.append("phone_nos", {
                                'phone': i['customer']['telephone'],
                                'is_primary_mobile_no': 1,


                            })
                            # Customer
                            guest.append("links", {
                                'link_doctype': 'Customer',
                                'link_name': c['guest_name'],
                                'link_title': c['guest_name'],

                            })

                            guest.insert()

                        transactionid = i['id']
                        night = a['nights']
                        qty = no_of_rooms * int(night)

                        # Transaction Id Check
                        sales_order = frappe.get_list(
                            'Sales Order', fields=['transactionid'])
                        check = {'transactionid': i['id']}

                        if check not in sales_order:
                            sales_order_api = frappe.get_doc({
                                "doctype": "Sales Order",
                                "company": company,
                                "customer": c['guest_name'],
                                "guest_cf": c['guest_name']+"-"+c['guest_name'],
                                "booking_type": "Online Booking",
                                "transactionid": transactionid,
                                "check_in_cf": c['arrival_date'],
                                "no_of_nights_cf": a['nights'],
                                "check_out_cf": c['departure_date'],
                                "no_of_guest_cf": no_of_guest,
                                "room_type_cf": c['id'],
                                "room_package_cf": m['mealplan'],
                                "number_of_room": no_of_rooms,
                                "room_rate_cf": c['totalbeforetax'],
                            })

                            sales_order_api.append("items", {
                                'item_code': m['mealplan'],
                                'item_name': m['mealplan'],
                                'qty': qty,
                                "reservation_date_from": c['arrival_date'],
                                "reservation_date_to": c['departure_date'],
                                "rate": c['totalbeforetax'],

                            })

                            sales_order_api.append("taxes", {
                                'charge_type': "Actual",
                                'account_head': "TAX 18% - "+abbr,
                                'rate': "0.00",
                                        'tax_amount': c['totaltax'],
                                        'description': "TAX 18% - "+abbr,

                            })

                            sales_order_api.insert()
                            sales_order_api.submit()
                            # frappe.msgprint("Data Inserted Successfully")

    else:
        frappe.msgprint("Auth Wrong")
