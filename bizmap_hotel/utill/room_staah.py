from unicodedata import name
import frappe
import json
from datetime import date, datetime, timedelta
import requests
from requests.structures import CaseInsensitiveDict


@frappe.whitelist(allow_guest=True)
def update_room():

        # r = room
        room_ty = frappe.db.sql("select room_type_code from `tabRoom Type HMS`")
        room_av = frappe.db.sql("select room_availability from `tabRoom Type HMS`")

        # First Data Update
        room_ty_0 = room_ty[0]
        room_ty_1=(','.join(room_ty_0))
        
        room_av_0 = room_av[0]
        room_av_1 =(','.join(room_av_0))

        # # Second Data Update
        # room_ty_01 = room_ty[1]
        # room_ty_2 =(','.join(room_ty_01))

        # room_av_01= room_av[1]
        # room_av_2 =(','.join(room_av_01))


        date = datetime.today().strftime('%Y-%m-%d')

        url = "https://kiviosandbox.staah.net/SUAPI/jservice/availability"

        headers = CaseInsensitiveDict()
        headers["Authorization"] = "Basic bzZVZndCVW86bnN5S05nZ1Y"
        headers["Content-Type"] = "application/json"

        data = {    
        
                "hotelid": "SP-1011",
                "room": [{
                        "roomid": room_ty_1,
                        "date": [{
                        "from": f"{date}",
                        "to": f"{date}",
                        "roomstosell": room_av_1
                        
                        }]
                }]
        
        }

        # data = json.dumps(data)
        # frappe.msgprint(data)

        response = requests.post(url, headers=headers,  data = json.dumps(data))
        if (response.status_code == 200):
                frappe.msgprint("Room Updated Successfully")
        else:
                frappe.msgprint("Auth Wrong")



