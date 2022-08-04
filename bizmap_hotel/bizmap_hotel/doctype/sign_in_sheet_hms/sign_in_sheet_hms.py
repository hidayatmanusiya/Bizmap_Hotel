# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import _
from datetime import datetime, timedelta
from frappe.utils import now_datetime
import frappe
import json

class SignInSheetHMS(Document):
	pass


@frappe.whitelist()
def fill_sign_sheet_name_to_room_folio(doc):
    doc =json.loads(doc)
    if doc.get('room_folio'):
       existing_room_folio=frappe.get_doc('Room Folio HMS',doc.get('room_folio'))
       if existing_room_folio.sign_in_sheet is None:
          existing_room_folio.sign_in_sheet=doc.get('name')
          existing_room_folio.save()
       else:
           frappe.throw(existing_room_folio.name,"SigIn sheet alrady Exixt")    
       
