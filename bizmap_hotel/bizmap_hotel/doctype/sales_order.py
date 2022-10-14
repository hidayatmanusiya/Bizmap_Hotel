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
                "check_out_cf":"check_out",
                "no_of_nights_cf":"quantity",
                "room_rate_cf":"room_rate",
                "contact_mobile":"customer_mobile",
                "contact_email": "customer_email"
              
            },
        }
           }, target_doc)
      
    return target_doc

@frappe.whitelist()
def doc_mapped_to_for_multiple_room_folio(doc):
    doc =json.loads(doc)
    existing_room_folio=frappe.db.get_value("Room Folio HMS",{'reservation':doc.get('name')},'name')
    if not existing_room_folio:
       for i in range(doc.get('number_of_room')):
           New_room_folio = frappe.new_doc('Room Folio HMS')
           New_room_folio.reservation = doc.get('name')
           New_room_folio.customer = doc.get('customer')
           New_room_folio.reservation_notes= doc.get('reservation_notes_cf')
           New_room_folio.room_type = doc.get('room_type_cf')
           New_room_folio.room_package = doc.get('room_package_cf')
           New_room_folio.room_rate = doc.get('room_rate_cf')
           New_room_folio.check_out=doc.get('check_out_cf')
           if doc.get("weekend_rate_cf"):
              New_room_folio.room_rate=doc.get("weekend_rate_cf")
           
           New_room_folio.insert(
            ignore_permissions=True,
            ignore_links=True,
            ignore_if_duplicate=True,
            ignore_mandatory=True
            )
           New_room_folio.run_method('submit')


def before_submit(doc,method):
       
    #check_room_avablity
    occupied_room_room_folio=[i.m for i in frappe.db.sql(f""" select COUNT(room_type)as m from `tabRoom Folio HMS` where check_out BETWEEN "{doc.check_in_cf}" AND "{doc.check_out_cf}" AND room_type='{doc.room_type_cf}'  And status="Checked Out" """, as_dict=1)]
    print("occupied_room",occupied_room_room_folio)
    total_room=[i.m for i in frappe.db.sql(f""" select COUNT(room_type) as m from `tabRoom HMS` where room_type="{doc.room_type_cf}" and  status!="Out Of Order"  """, as_dict=1)]
    print("total_room",total_room)
    
  
    occupied_booking_room_from_so=[0 if i.m  is None else i.m for i in frappe.db.sql(f""" select  SUM(number_of_room) as m from `tabSales Order`
where check_in_cf  between "{doc.check_in_cf}" and "{doc.check_out_cf}" or check_out_cf between "{doc.check_in_cf}" and "{doc.check_out_cf}" or check_out_cf > "{doc.check_out_cf}" and room_type_cf="3534700000000000003" And status!="Cancelled" """, as_dict=1)]

    if occupied_booking_room_from_so[0]<=total_room[0]:
        avalible_room = total_room[0]- occupied_booking_room_from_so[0]
        print("occupied_booking_room_from_so+++++++++++",occupied_booking_room_from_so)
        update_room_type=frappe.get_doc("Room Type HMS",doc.room_type_cf)
        update_room_type.total_room=total_room[0]
        update_room_type.available_room_= avalible_room
        update_room_type.save()

    else:
         frappe.throw("can't create more")   
    
       

 
 
