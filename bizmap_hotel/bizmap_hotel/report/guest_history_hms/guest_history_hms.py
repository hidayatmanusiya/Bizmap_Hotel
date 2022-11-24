# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    data =prepare_data(filters)
    columns=get_columns(filters)
    return columns, data
	
	
	
	
	
def get_columns(filters=None):
        return[
            
            {
            "label":"Guest Name",
            "fieldtype":"Data",
            "fieldname":"guest_name",
             "width":150
            },
            {
            "label":"Customer Name",
            "fieldtype":"Data",
            "fieldname":"customer_name",
             "width":120
            },
            {
            "label":"Mobile",
            "fieldtype":"Data",
            "fieldname":"mobile",
             "width":150
            },
            {
            "label":"Email",
            "fieldtype":"Data",
            "fieldname":"email",
             "width":150
            },
            {
            "label":"Check In",
            "fieldtype":"Datetime",
            "fieldname":"check_in",
             "width":160
            },
            {
            "label":"Check Out",
            "fieldtype":"Datetime",
            "fieldname":"check_out",
             "width":160
            },
            {
            "label":"Room",
            "fieldtype":"Data",
            "fieldname":"room",
             "width":150
            },
            {
            "label":"Room Type",
            "fieldtype":"Data",
            "fieldname":"room_type",
             "width":150
            },{
            "label":"Charges",
            "fieldtype":"float",
            "fieldname":"charges",
             "width":150
            },
        
        ]	
        
def prepare_data(filters):
    data = []
    fltr={}
    
    if filters.get("check_in"):
       fltr.update({"check_in":filters.get("check_in")})
    for i in frappe.db.sql(f""" Select name,customer,room_type,room_no,reservation,check_in,check_out,total_charges,customer_mobile,customer_email from `tabRoom Folio HMS` WHERE check_in BETWEEN '{filters.get("check_in")}'and CURDATE()""",as_dict=1):
        row={}
        row.update(i)
        row.update({"guest_name":frappe.db.get_value("Sales Order",{"name":i.reservation},"guest_cf"),"customer_name":i.customer,"mobile":i.customer_mobile,"email":i.customer_email,"check_in":i.check_in,"check_out":i.check_out,"room":i.room_no,"room_type":i.room_type,"charges":i.total_charges,})
        data.append(row)
       
    return data   
            
