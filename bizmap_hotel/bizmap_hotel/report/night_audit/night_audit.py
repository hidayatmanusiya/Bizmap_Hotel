# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

# import frappe


def execute(filters=None):
	columns, data = [], []
	return columns, data
	
	
def get_columns(filters=None):
        return [ 
        {
        "label":"Room No",
        "fieldtype":"Data",
        "fieldname":"room_no",
        "width":150
        },
        {
        "label":"Room Type",
        "fieldtype":"Data",
        "fieldname":"room_type",
        "width":150
        },
        {
        "label":"Status",
        "fieldtype":"Data",
        "fieldname":"status",
        "width":150
        },
        {
        "label":"Folio",
        "fieldtype":"Data",
        "fieldname":"folio",
        "width":150
        },
        {
        "label":"Guest",
        "fieldtype":"Data",
        "fieldname":"guest",
        "width":150
        },
        {
        "label":"In",
        "fieldtype":"Datetime",
        "fieldname":"in",
        "width":150
        },
        {
        "label":"Out",
        "fieldtype":"Datetime",
        "fieldname":"out",
        "width":150
        },
        {
        "label":"Customer",
        "fieldtype":"Data",
        "fieldname":"customer",
        "width":150
        },
        {
        "label":"Invoice",
        "fieldtype":"Data",
        "fieldname":"invoice",
        "width":150
        },
        {
        "label":"Outstanding",
        "fieldtype":"Data",
        "fieldname":"outstanding",
        "width":150
        },
        {
        "label":"Total",
        "fieldtype":"flot",
        "fieldname":"total",
        "width":150
        }
        
          ]	
          
def prepare_data(filters=None):
    data = []
    fltr={}


         
