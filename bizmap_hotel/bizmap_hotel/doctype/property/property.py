# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
class Property(Document):
	pass
	
@frappe.whitelist()	
def get_adresss(doc):
    doc = json.loads(doc)
    if doc.get("address"):
       address=frappe.db.get_value("Address",{"name":doc.get("address")},["address_type","address_line1","address_line2","city","pincode","state","country"])
       Address_list=' '.join(i for i in address if i is not None)
       #Address_list=' '.join(i for i in address if i not in ' ')
       return Address_list    	
       
       
       
@frappe.whitelist()	       
def contact_list(doctype, txt, searchfield, start, page_len, filters):
    address_title=frappe.db.get_value("Address",{"name":filters.get("address")},'address_title')
    contact_lst= [i.parent for i in frappe.db.sql(f""" select parent from `tabDynamic Link`  where link_name="{address_title}" """,as_dict=1)]
    
    return [(i,) for i in contact_lst]
    
@frappe.whitelist()	       
def get_mobile_emalil_frm_contact(doc):
    doc = json.loads(doc)
    mobile_phone ={}
    if doc.get("contact"):
       get_phone=[mobile_phone.update({"phone":i.phone}) for i in frappe.db.sql(f""" select phone from `tabContact Phone` where parent="{doc.get("contact")}" """,as_dict=1)]
       get_email= [mobile_phone.update({"email_id":i.email_id}) for i in frappe.db.sql(f""" select email_id from `tabContact Email` where parent="{doc.get("contact")}" """,as_dict=1)]
       return mobile_phone
 
 
 
 
 
