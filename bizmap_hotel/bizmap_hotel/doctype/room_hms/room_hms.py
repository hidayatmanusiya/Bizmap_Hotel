# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoomHMS(Document):
	pass
	


def validate(doc,method):
    room_hms_total=frappe.db.count('Room HMS', {'room_type': doc.room_type})
    room_type_hms=frappe.db.get_value('Room Type HMS', {'room_type_code': doc.room_type},"total_room")
    if room_type_hms is not None:
       for i in frappe.db.get_list('Room HMS',"room_no"):
           if room_type_hms<= room_hms_total and i.room_no!=doc.room_no:
              frappe.throw(f"Total Room of Room Type {doc.room_type} has  {room_type_hms} Room. you Can't Create More")
          
          
          
             
	                                                                                                           
