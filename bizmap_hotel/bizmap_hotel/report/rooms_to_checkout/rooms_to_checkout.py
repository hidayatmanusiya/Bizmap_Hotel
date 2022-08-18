# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta


def execute(filters=None):
    data = prepare_data(filters)
    columns = get_columns(filters)
    return columns, data
	
	
	
def get_columns(filters=None):
        return [
        {
        "label":"Folio",
        "fieldtype":"Data",
        "fieldname":"folio",
        "width":150
        },
        {
        "label":"Room Type",
        "fieldtype":"Data",
        "fieldname":"room_type",
        "width":120
        
        },
        {
        "label":"Room#",
        "fieldtype":"Data",
        "fieldname":"room",
        "width":120
        },
        {
         "label":"Customer",
         "fieldtype":"Data",
         "fieldname":"customer",
         "width":120
        },
        {
          "label":"Guest",
          "fieldtype":"Data",
          "fieldname":"guest",
          "width":120
        
        },
        {
         "label":"Contact",
         "fieldtype":"int",
         "fieldname":"contact",
         "width":150
        },
        {
        "label":"Check In",
        "fieldtype":"Datetime",
        "fieldname":"check_in",
        "width":150
        
        },
        {
        "label":"Check Out",
        "fieldtype":"Datetime",
        "fieldname":"check_out",
        "width":150
        },
        {
         "label":"Status",
         "fieldtype":"Data",
         "fieldname":"status",
         "width":150
        
        }
       ]
       
       
def prepare_data(filters):
    data = []
    fltr={}
    
    if filters.get("check_out"):
       fltr.update({"check_out":filters.get("check_out")})
       print(fltr) 
       for i in frappe.db.sql(f""" Select name,customer,room_type,room_no,reservation,check_in,check_out,status from `tabRoom Folio HMS` WHERE check_out LIKE '%{filters.get("check_out")}%' """,as_dict=1):
        row={}
        row.update(i)
        row.update({"folio":i.name,"customer":i.customer,"room_type":i.room_type,"room":i.room_no,"guest":frappe.db.get_value("Sales Order",{"name":i.reservation},"guest_cf"),"check_in":i.check_in,"check_out":i.check_out,"status":i.status})
        data.append(row)
        
    return data
    
    
    
    




           	
