# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
class RoomCleaning(Document):
	pass
	
	

def before_submit(doc,method):
    validate_room_no(doc)
    if doc.room_no:
       room_no=frappe.get_doc("Room HMS",doc.get("room_no"))
       room_no.status="Availabel"
       room_no.save()	
       
@frappe.whitelist()
def room_no_fltr(doctype, txt, searchfield, start, page_len, filters):
    if txt:
       filters.update({"name": ("like", "{0}%".format(txt))})
    return frappe.get_all('Room HMS',filters=filters,fields=['name'],as_list=1)
       
       
def validate_room_no(doc):
    room_no=frappe.db.sql(f"""  SELECT CASE WHEN EXISTS (
    SELECT *
    FROM `tabRoom HMS`
    WHERE room_type = "{doc.room_type}"
    and name="{doc.room_no}"
)   
THEN  1 ELSE  0 end """,as_dict=0)
    value=re.sub(r"[\([{,})\]]","",str(room_no))
    if value == "0":
       frappe.throw(f" '{doc.room_no}' is not belongs to room_type '{doc.room_type}' please select proper Room No ") 
       
             
