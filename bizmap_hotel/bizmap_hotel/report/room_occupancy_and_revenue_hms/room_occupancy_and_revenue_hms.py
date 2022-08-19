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
    return columns,data
	
	

def get_columns(filters=None):
        return [
          {
             "label": "Room Type",
	     "fieldtype": "Link",
	     "fieldname": "room_type",
	     'width':120,
	     "options":"Room Type HMS"
          },
          {
          "label":"No of Rooms",
          "fieldtype":"int",
          "fieldname":"no_of_rooms",
          "width"  :120
          },
          {
          "label":"Guest Name",
          "fieldtype":"Data",
          "width":150
          },
          {
          
           "label":"No of People",
           "fieldtype":"int",
           "fieldname":"no_of_people",
           "Width":120
          
          
          },
          {
            "label":"Plan(packages)",
            "fieldtype":"Data",
            "fieldname":"plan"
          
          
          },
          {
            "label":"Occupancy",
            "fieldtype":"Data",
            "fieldname":"occupancy",
            "width":120
          
          },
          {
          "label":"Empty",
          "fieldtype":"empty",
          "fieldtype":"Data",
          "width":120
          
          },
          {

          "label":"Avg Occupancy per Day",
          "fieldtype":"int",
          "width":150
          
          },
          {
          "label":"Avg Empty",
          "fieldtype":"int",
          "width":120
          
          },
          {
           "label":"% Occupancy",
           "fieldtype":"float",
           "width":120
          
          },
          {
          "label":"Normal Room Rate",
          "fieldtype":"Currency",
          "fieldname":"room_rate",
          "width":150
          },
           {
          "label":"Special Room Rate",
          "fieldtype":"Currency",
          "fieldname":"special_room_rate",
          "width":150
          },
          {
           "label":"Revenue",
           "fieldtype":"Currency",
           "fieldname":"revenue",
           "width":150
          
          }
        
        ]
        
        
        
def prepare_data(filters):
    data = []
    fltr={}
    if filters.get("company"):
        fltr.update({"company":filters.get("company")})
    if filters.get("customer"):
       fltr.update({"customer":filters.get("customer")})
    
    
    for i in frappe.get_all("Room Type HMS",filters=fltr,fields=['name','service_item']):
        row={}
        row.update(i)
        #print(i.name)
        Occupancy_count=[j.m for j in frappe.db.sql(f""" select COUNT(name) as m from `tabRoom Folio HMS` where check_out BETWEEN "{filters.get("from_date")}" AND "{filters.get("to_date")}" AND room_type='{i.name}' """, as_dict=1)]
        Empty_count=frappe.db.count("Room HMS",{"room_type":i.name})-Occupancy_count[0]
        
        row.update({"room_type":i.name,"no_of_rooms":frappe.db.count("Room HMS",{"room_type":i.name}),"room_rate":frappe.db.get_value("Item Price",{"item_code":i.service_item},"price_list_rate"),"occupancy":Occupancy_count[0],"empty":Empty_count})
        data.append(row)
        #print(data)
        #print(filters.get("from_date"))
    return data
    


        	
