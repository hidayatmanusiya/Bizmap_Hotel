# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class RoomFolioHMS(Document):
	pass
	
	
@frappe.whitelist()	
def map_sign_in_sheet_with_room_folio(source_name, target_doc=None):
    target_doc = get_mapped_doc("Room Folio HMS", source_name,
       {
        "Room Folio HMS": {
            "doctype": "Sign In Sheet HMS",
            "field_map": {
                "name": "folio",
                
              
            },
        }
           }, target_doc)
      
    return target_doc
    
    	
