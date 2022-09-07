from venv import create
import frappe
import requests
import json
from datetime import date, datetime, timedelta
import requests
from requests.structures import CaseInsensitiveDict


@frappe.whitelist(allow_guest=True)
def insertbooking():

    url = "https://live.ipms247.com/pmsinterface/pms_connectivity.php"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/xml"
    headers["Content-Type"] = "application/xml"

    data = """
    {
        "RES_Request": {
                "Request_Type": "Bookings",
                "Authentication": {
                        "HotelCode": "35347",
                        "AuthCode": "7637120501df617d17-282d-11ed-8"
                    }
            }
    }
    """

    response = requests.post(url, headers=headers, data=data)
    if (response.status_code == 200):
        tr = response.json()
        j = json.loads(json.dumps(tr))
        for i in j['Reservations']['Reservation']:
            for r in i['BookingTran']: 

                  
                stagging = frappe.new_doc("Sales Order")
                stagging.guest = r['FirstName']
                stagging.transactionid = r['TransactionId']
                stagging.createdatetime = r['Createdatetime']
                stagging.status = r['Status']
                stagging.isconfirmed = r['IsConfirmed']
                stagging.packagename = r['PackageName']
                stagging.check_in = r['Start']
                stagging.check_out = r['End']
                stagging.total_amount = r['TotalAmountAfterTax'], 
                stagging.gender = r['Gender'],
                stagging.mobile = r['Mobile'],             
                # Create customer 
                customer_list = frappe.get_list('Customer', fields=['customer_name'])
                check = {'customer_name': stagging.guest}
                if check not in customer_list:
                    customer = frappe.get_doc({
                        "doctype": "Customer",
                        "customer_name": stagging.guest,
                        "customer_group": 'Individual',
                        "territory":'India'
                    })
                    customer.insert()

                # Create contact
                contact_list = frappe.get_list('Contact', fields=['first_name'])
                check = {'first_name': stagging.guest}
                if check not in contact_list:
                    guest = frappe.get_doc({
                        "doctype": "Contact",
                        "first_name": stagging.guest,
                        # "last_name": stagging.guest,
                        "gender":'Male'
                        
                    })
                    guest.append("phone_nos",{
                                            'phone':'+91 9724503250',
                                            'is_primary_mobile_no':1,
                                            
                                            
                                        })
                    guest.append("links",{
                                            'link_doctype':'Customer',
                                            'link_name':stagging.guest,
                                            'link_title':stagging.guest,
                                            
                                        })

                    guest.insert()

                 # Create Sales Order
                sales_order = frappe.get_list('Sales Order', fields=['transactionid'])
                check = {'transactionid': stagging.transactionid}    
                
                if check not in sales_order:
                    sales_order_api = frappe.get_doc({
                        "doctype": "Sales Order",
                        "customer": r['FirstName'],
                        "guest_cf":r['FirstName']+"-"+r['FirstName'],
                        "transactionid": r['TransactionId'],
                        "check_in_cf": r['Start'],
                        "no_of_nights_cf": 1,
                        "check_out_cf": r['End'],
                        "no_of_guest_cf": 1,
                        "room_type_cf":"European Plan",
                        "room_package_cf":r['RateplanName'],
                        "number_of_room": 1, 
                        "room_rate_cf": r['TotalAmountBeforeTax'],  
                        # "taxes_and_charges":"Output GST In-state - B"                   
                        
                })      
                    sales_order_api.append("items",{
                                            'item_code':r['RateplanName'],
                                            'item_name':r['RateplanName'],
                                            'qty':1,
                                            "reservation_date_from": r['Start'],
                                            "reservation_date_to": r['End'],
                                            
                                        })
                    for t in r['TaxDeatil']:
                        sales_order_api.append("taxes",{
                                            'charge_type':"Actual",
                                            'account_head':t['TaxName']+" "+"- B",
                                            'rate':"0.00",
                                            'tax_amount':t['TaxAmount'],
                                            # "total": r['TotalAmountAfterTax'],
                                            'description':t['TaxName']+" "+"- B",
                                        })                    

                    sales_order_api.insert() 
                    sales_order_api.submit() 
                    # frappe.msgprint("Data Inserted Successfully")

    else:
        frappe.msgprint("Auth Wrong")



