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



def before_submit(doc,method):
    if doc.room_folio:
       existing_room_folio=frappe.get_doc('Room Folio HMS',doc.room_folio)
       if existing_room_folio.sign_in_sheet is None:
          existing_room_folio.sign_in_sheet= doc.name
          existing_room_folio.save()
          existing_room_folio.reload()
       else:
           frappe.throw(f"SigIn sheet alrady Exist in '{existing_room_folio.name}' ")    
       
