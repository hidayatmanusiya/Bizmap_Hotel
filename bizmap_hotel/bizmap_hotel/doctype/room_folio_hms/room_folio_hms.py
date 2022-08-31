# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json
from datetime import datetime ,timedelta,date
from frappe.utils import getdate
import frappe.utils
from frappe.utils import now
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
    
@frappe.whitelist()    	
def description_for_sales_books(name):
    decs= frappe.db.sql(f"""
    SELECT description from `tabSales Order Item` where parent='{name}'
 """, as_dict=1)
    return decs    	
    
    
    
@frappe.whitelist()    
def room_folio_sales_invoice(source_name, target_doc=None):    
    target_doc = get_mapped_doc("Room Folio HMS", source_name,
       {
        "Room Folio HMS": {
            "doctype": "Sales Invoice",
            "field_map": {
                "name": "room_folio_ref",
                "customer":"customer"
                 #"name":"room_folio"
                
              
            },
        }
           }, target_doc)
      
    return target_doc

   
@frappe.whitelist()    
def sales_order_item_transfer_to_sales_invoice(room_folio_ref):
    sales_order_child_itm=[]
    if room_folio_ref:
       sales_order_ref =[i.sales_order for i in frappe.db.sql(f"""select sales_order from `tabSales Book Item` where parent='{room_folio_ref}' """,as_dict=1)]
       #print(sales_order_ref)
      #qty=frappe.get_doc('Sales Invoice',room_folio_ref)
      
       for i in sales_order_ref:
           sales_order_itm=frappe.db.sql(f"""select a.item_code,a.uom,a.description,a.item_name,m.total_qty,a.conversion_factor,a.item_tax_template, m.room_rate_cf,c.quantity,m.name from `tabSales Order` as m inner join `tabSales Order Item` as a inner join `tabRoom Folio HMS` as c on a.parent=m.name  where m.name="{i}" and c.name='{room_folio_ref}' """,as_dict=0)
           sales_order_child_itm.append(sales_order_itm)
    return sales_order_child_itm
    
    
@frappe.whitelist()    
def checkout_minus_checkin_days_diffrence(doc):
    doc = json.loads(doc)
    if doc.get('check_in') and doc.get('check_out'):
        ChekIn=frappe.utils.formatdate(str(doc.get('check_in')),'yyyy-MM-dd')
        ChekOut=frappe.utils.formatdate(str(doc.get('check_out')),'yyyy-MM-dd')
        check_in=datetime.strptime(ChekIn,"%Y-%m-%d")
        check_out=datetime. strptime(ChekOut,"%Y-%m-%d")
        checkin_formate=date(check_in.year,check_in.month,check_in.day)
        checkout_formate=date(check_out.year,check_out.month,check_out.day)
        if ChekIn == ChekOut:
           return 1
        return (checkout_formate-checkin_formate).days
    
        
    
    
@frappe.whitelist()    
def payment_entry(doc):
    doc=json.loads(doc)
    get_value_frm_sale_order =frappe.db.sql(f""" select name,customer,guest_cf,total from `tabSales Order` where name='{doc.get('room_folio_reference')}' """,as_dict=0)
    print(get_value_frm_sale_order)
    return get_value_frm_sale_order
    
    
@frappe.whitelist()
def check_in_button(doc):
    doc =json.loads(doc)
    if doc.get('name'):
       frappe.db.set_value("Room Folio HMS", {"name": doc.get('name')},{ "status":"Checked In"})
      
    


@frappe.whitelist()
def check_out_button(doc):
    doc =json.loads(doc)
    if doc.get('name'):
       frappe.db.set_value("Room Folio HMS", {"name": doc.get('name')},{ "status":"Checked Out","check_out":now()})


@frappe.whitelist()
def get_sales_order(doc):
    #sales_order_list =[s.get('sales_order') for s in frappe.db.get_list("Sales Invoice Item", {'docstatus':1}, 'sales_order')]
    
    #print(sales_order_list)
    #return sales_order_list if len(sales_order_list)>0 else 0
    doc =json.loads(doc)
    sales_order_invoice=[i.name for i in frappe.db.sql(f""" select a.name from `tabSales Order` as a inner join `tabSales Invoice Item` as m inner join `tabSales Invoice` as p  where a.name=m.sales_order and p.customer='{doc.get("customer")}' """,as_dict=1)]
   # print(sales_order_invoice)
    for i in sales_order_invoice:
        sales_invoice_not_md=[j.name for j in frappe.db.sql(f""" select name from `tabSales Order` where name != "{sales_order_invoice}" and customer='{doc.get("customer")}' """,as_dict=1)]
       # print(sales_invoice_not_md)
       
        s1=set(sales_order_invoice)
        s2=set(sales_invoice_not_md)
        array=list(s2.difference(s1))
        print(sales_invoice_not_md)
        return array
    #for j in frappe.db.sql(""" select name from `tabSales Order` """,as_dict=1):
    
    #B=frappe.db.sql(f""" select m.sales_order from `tabSales Order`as S inner join `tabSales Invoice` as a inner join `tabSales Invoice Item` as m on m.parent=a.name where sales_order="{j.name}" """,as_dict=1)
    #if not B:
     #  return B
    
    
    
    
