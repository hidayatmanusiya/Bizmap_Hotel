# -*- coding: utf-8 -*-
# Copyright (c) 2020, bizmap technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime ,timedelta
import calendar
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from frappe.model.mapper import get_mapped_doc
import json
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc




@frappe.whitelist()
def check_out_date(doc):
    doc=json.loads(doc)
    if doc.get('no_of_nights_cf') and doc.get('check_in_cf'):
       check_in=str(doc.get('check_in_cf'))
       checkIn_strp=datetime. strptime(check_in,"%Y-%m-%d")
       checkInformate=datetime(checkIn_strp.year,checkIn_strp.month,checkIn_strp.day)
       checkOutdate = checkInformate + relativedelta(days=(int(doc.get('no_of_nights_cf'))))
       return checkOutdate.date()


@frappe.whitelist()
def insert_items(doc):
    doc=json.loads(doc)
    room_pakage=doc.get('room_package_cf')
    no_of_night= float(doc.get('no_of_nights_cf')) * doc.get('number_of_room') 
    check_in_date=doc.get('check_in_cf')
    check_out_date = doc.get('check_out_cf')
    room_package_description=frappe.db.get_value('Item',{'name':doc.get('room_package_cf')},['description','stock_uom'])
    return room_pakage,no_of_night,check_in_date,check_out_date,room_package_description

@frappe.whitelist()
def doc_mapped_to_room_folia(source_name, target_doc=None):
    #print(doc.name)
    target_doc = get_mapped_doc("Sales Order", source_name,
       {
        "Sales Order": {
            "doctype": "Room Folio HMS",
            "field_map": {
                "name": "reservation",
                "customer":"customer",
                "reservation_notes_cf":"reservation_notes",
                "room_type_cf":"room_type",
                "room_no_cf":"room_no",
                "room_package_cf":"room_package",
                "room_rate_cf":"room_rate"
              
            },
        }
           }, target_doc)
      
    return target_doc

@frappe.whitelist()
def doc_mapped_to_for_multiple_room_folio(doc):
    doc =json.loads(doc)
    for i in range(doc.get('number_of_room')):
        New_room_folio = frappe.new_doc('Room Folio HMS')
        New_room_folio.reservation = doc.get('name')
        New_room_folio.customer = doc.get('customer')
        New_room_folio.reservation_notes= doc.get('reservation_notes_cf')
        New_room_folio.room_type = doc.get('room_type_cf')
        New_room_folio.room_package = doc.get('room_package_cf')
        New_room_folio.room_rate = doc.get('room_rate')
        New_room_folio.insert(
           ignore_permissions=True,
           ignore_links=True,
           ignore_if_duplicate=True,
           ignore_mandatory=True
        
        )
    
