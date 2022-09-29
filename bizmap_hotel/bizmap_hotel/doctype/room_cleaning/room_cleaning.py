# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoomCleaning(Document):
	pass
	
	

def before_submit(doc,method):
    if doc.room_no:
       room_no=frappe.get_doc("Room HMS",doc.get("room_no"))
       room_no.status="Availabel"
       room_no.save()	
