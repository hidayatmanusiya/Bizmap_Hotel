# Copyright (c) 2022, BizMap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json
import time
import re
from datetime import datetime ,timedelta,date
from frappe.utils import getdate
import frappe.utils
from frappe.utils import now
class RoomFolioHMS(Document):
	pass
	
#mapping SHingIn sheet from room Folio data	
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
#fetching dicription from sales order and inserting on room folio  sale order itm child tbl     
@frappe.whitelist()    	
def description_for_sales_books(name):
    decs= frappe.db.sql(f"""
    SELECT description from `tabSales Order Item` where parent='{name}'
 """, as_dict=1)
    return decs    	
    
    
    
#@frappe.whitelist()    
#def room_folio_sales_invoice(source_name, target_doc=None):    
#    target_doc = get_mapped_doc("Room Folio HMS", source_name,
#       {
#        "Room Folio HMS": {
#            "doctype": "Sales Invoice",
#            "field_map": {
#                "name": "room_folio_ref",
#                "customer":"customer",
#                 #"name":"room_folio"
#                "total_advance_paid":"total_advance",
#                "outstanding_charges":"outstanding_amount"
#                
#              
#            },
#        }
#           }, target_doc)
#      
#    return target_doc

   
#@frappe.whitelist()    
#def sales_order_item_transfer_to_sales_invoice(room_folio_ref):
#    sales_order_child_itm=[]
#    if room_folio_ref:
#       sales_order_ref =[i.sales_order for i in frappe.db.sql(f"""select sales_order from `tabSales Book Item` where parent='{room_folio_ref}' """,as_dict=1)]
      
#       for i in sales_order_ref:
#           sales_order_itm=frappe.db.sql(f"""select a.item_code,a.uom,a.description,a.item_name,m.total_qty,a.conversion_factor,a.item_tax_template, m.room_rate_cf,c.quantity,m.name from `tabSales Order` as m inner join `tabSales Order Item` as a inner join `tabRoom Folio HMS` as c on a.parent=m.name  where m.name="{i}" and c.name='{room_folio_ref}' """,as_dict=0)
#           sales_order_child_itm.append(sales_order_itm)
#    return sales_order_child_itm


#fetching sales order data from room folio sale_itm_tb including tax
@frappe.whitelist()
def sales_order_item_transfer_to_sales_invoice(doc):
    doc = json.loads(doc)
    if doc.get("name"):
       sales_invoice = frappe.new_doc('Sales Invoice')
       sales_invoice.customer = doc.get("customer")
       sales_invoice.room_folio = doc.get("name")
       sales_invoice.total_advance = doc.get("total_advance_paid")
       sales_invoice.outstanding_amount = doc.get("outstanding_charges")
       sales_invoice.due_date = frappe.utils.nowdate()
       sales_order_ref =[i.sales_order for i in frappe.db.sql(f"""select sales_order from `tabSales Book Item` where parent='{doc.get("name")}' """,as_dict=1)]
       
       defaut_incm_account=frappe.db.get_value("Company",{"name":doc.get("company")},['default_income_account'])
       if sales_order_ref:
          for i in sales_order_ref:
              sales_order_itm=frappe.db.sql(f"""select a.item_code,a.uom,a.description,a.item_name,m.total_qty,a.conversion_factor,a.item_tax_template, m.room_rate_cf,c.quantity,m.name from `tabSales Order` as m inner join `tabSales Order Item` as a inner join `tabRoom Folio HMS` as c on a.parent=m.name  where m.name="{i}" and c.name='{doc.get("name")}' """,as_dict=1)
                 
              sales_tx_charges=frappe.db.sql(f""" select charge_type,account_head,rate from `tabSales Taxes and Charges` where parent ="{i}" """,as_dict=1) # it getting all info of  sale order from above list
              
              for j in  sales_order_itm:
                  sales_invoice_itm= sales_invoice.append('items',{})
                  sales_invoice_itm.item_code = j.item_code
                  sales_invoice_itm.item_name = j.item_name
                  sales_invoice_itm.description = j.description
                  sales_invoice_itm.uom = j.uom
                  sales_invoice_itm.qty = j.quantity
                  sales_invoice_itm.sales_order = j.name
                  if defaut_incm_account:
                     sales_invoice_itm.income_account = defaut_incm_account
              if sales_tx_charges:       
                 for tax in sales_tx_charges:   
                     taxChild = sales_invoice.append('taxes',{})
                     taxChild.charge_type  = tax.charge_type
                     taxChild.account_head = tax.account_head
                     taxChild.rate =   tax.rate
          sales_invoice.insert(
                     ignore_permissions=True,
                     ignore_links=True,
                     ignore_if_duplicate=True,
                     ignore_mandatory=True
                    )   
          return sales_invoice.name

#from sales tax and Charges child table from sales order fetch value in sales tax and Charges in sale invoice 
#js code is on sales_invoice.js 
#@frappe.whitelist()
#def sales_order_sale_tax_to_sales_invoice_sale_tax(room_folio_ref):
#    sales_txt=[]
#    if room_folio_ref:
#       sales_order_ref =[i.sales_order for i in frappe.db.sql(f"""select sales_order from `tabSales Book Item` where parent='{room_folio_ref}' """,as_dict=1)] #here it take  sales order from room folio sales book itm table.
       
#       for i in sales_order_ref:
#           sales_tx_charges=frappe.db.sql(f""" select charge_type,account_head,rate from `tabSales Taxes and Charges` where parent ="{i}" """,as_dict=1) # it getting all info of  sale order from above list
#           sales_txt.append(sales_tx_charges)
#    return  sales_txt          
    
    
#getting diffrence between check-in and check-out date on room folio check-out btn or extending or reducing check-out dates
#In check-out field on room_folio_hms    
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
    

#@frappe.whitelist()    
#def payment_entry(doc):
#    doc=json.loads(doc)
#    sale_order_value=[]
#    sales_order_ref =[i.sales_order for i in frappe.db.sql(f"""select sales_order from `tabSales Book Item` where parent='{doc.get('name')}' """,as_dict=1)]
#    for i in sales_order_ref:
#        get_value_frm_sale_order =frappe.db.sql(f""" select name,customer,guest_cf,grand_total from `tabSales Order` where name="{i}" """,as_dict=1)
#        sale_order_value.append(get_value_frm_sale_order)
#    print(sale_order_value)
#    return sale_order_value


    
@frappe.whitelist()
def room_cleanig_doc(doc):
    doc=json.loads(doc)
    room_cleanig = frappe.new_doc('Room Cleaning') #On Room Folio check-out Click it will Create Room Cleanig Document
    room_cleanig.room_type=doc.get("room_type")
    room_cleanig.room_no=doc.get("room_no")
    room_cleanig.save()
    if doc.get("room_no"):
       room_no=frappe.get_doc("Room HMS",doc.get("room_no"))
       room_no.status="Dirty" # its update status of Allocated Room No in Room HMS master to Dirty
       room_no.db_update()
       #room_no.save()
    time.sleep(1)
    frappe.msgprint(f"Room Cleanig document created. {room_cleanig.name} has been Marked As dirty room please assign for cleaning ",[room_cleanig.name])
    return room_cleanig.name
  
    
def on_change(doc,method):
    room_no=frappe.db.sql(f"""  SELECT CASE WHEN EXISTS (
    SELECT *
    FROM `tabRoom HMS`
    WHERE room_type = "{doc.room_type}"
    and name="{doc.room_no}"
)   
THEN  1 ELSE  0 end """,as_dict=0) #to avoid pasting diffrent room no from diffrent room type in Room No field in Room Folio
    value=re.sub(r"[\([{,})\]]","",str(room_no))
    if value == "0" and doc.room_no:
       frappe.throw(f" '{doc.room_no}' is not belongs to room_type '{doc.room_type}' please select proper Room No ")
    non_existing_so=[] # from here to check duplicate so in booked sale tbl 
    for ma in frappe.get_all("Room Folio HMS",{"reservation":doc.reservation},"name"):
        booked_sale_tbl=[d.sales_order for d in frappe.get_all("Sales Book Item",{"parent":ma.name},['sales_order'])]
        for i in booked_sale_tbl:
            if i not in non_existing_so:
               non_existing_so.append(i)
            else:
                frappe.throw("Sales Order <b>{0}</b> already Exists in Sales Book Item Remove Duplicate from table <b>{1}</b>".format(i,ma.name))   
      
#It returnig Sales order Customer, Guest and Total Amount and inserting in Pyment Entry Form 
#js Written in pyment_entry.js from to insert in form    
@frappe.whitelist()
def payment_entry_from_room_folio(doc):
    doc=json.loads(doc)
    Pyment_Entry = frappe.new_doc("Payment Entry")
    Pyment_Entry.payment_type='Receive'
    Pyment_Entry.naming_series='ACC-PAY-.YYYY.-'
    Pyment_Entry.room_folio_reference= doc.get("name")
    Pyment_Entry.party_type='Customer'
    #Pyment_Entry.posting_date=frappe.datetime.nowdate()
    Pyment_Entry.party=doc.get("customer")
    Pyment_Entry.contact_person=doc.get("guest")
    Pyment_Entry.received_amount="  "
    #Pyment_Entry.target_exchange_rate=1.0
    Pyment_Entry.paid_to = frappe.db.get_value("Company",{"name":doc.get("company")},"default_bank_account")
    Pyment_Entry.paid_amount = doc.get("total_charges")
    Pyment_Entry.reference_no="    "
    Pyment_Entry.reference_date= frappe.utils.nowdate()
    Pyment_Entry.references=[]
    if doc.get("sales_book_item"):
       for i in [i.sales_order for i in frappe.db.sql(f"""select sales_order from `tabSales Book Item` where parent='{doc.get('name')}' """,as_dict=1)]:
           get_value_frm_sale_order =frappe.db.sql(f""" select name,customer,guest_cf,grand_total from `tabSales Order` where name="{i}" """,as_dict=1)
           for so in get_value_frm_sale_order:
                        
               pay_ref =Pyment_Entry.append('references',{})
               pay_ref.reference_doctype = "Sales Order"
               pay_ref.reference_name = so.name
               pay_ref.total_amount = so.grand_total
               pay_ref.outstanding_amount = so.grand_total
               pay_ref.allocated_amount = so.grand_total
    
    Pyment_Entry.insert(
             ignore_permissions=True,
             ignore_links=True,
             ignore_if_duplicate=True,
             ignore_mandatory=True
    )
    return Pyment_Entry.name
    




#this function is returning those sales order of customer whose sales invoice is not made.
#this sales order are displying in Multiselect dialogbox  on Room Folio HMS
#after select these SO can insert in sales book itm table in Room Folio
#Note js for this function calling from Folder room_folio_js's js file not Public's room_folio_js file 
@frappe.whitelist()
def get_sales_order(doc):
    doc =json.loads(doc)
    sales_order_without_invoice_list=[]
    date_range=frappe.db.get_value("Sales Order",{"name":doc.get("reservation")},['check_in_cf','check_out_cf'])
    if date_range is not None:
       sales_order=[i.name for i in frappe.db.sql(f""" select name from `tabSales Order` where check_in_cf and check_out_cf between "{date_range[0]}" and "{date_range[1]}" and contact_email='{doc.get("customer_email")}' """,as_dict=1)]
       for so in sales_order:
           sales_order_with_invoice=[i.sales_order for i in frappe.db.sql(f""" select sales_order from `tabSales Invoice Item` where sales_order="{so}" """,as_dict=1)]
      
           if so not in sales_order_with_invoice:
              sales_order_without_invoice_list.append(so)
    return sales_order_without_invoice_list
            
#on Check-In In Room Folio HMS this function Updating 
#status of allocated Room No. In Room HMS master to Occupied          
@frappe.whitelist()               
def room_master_status(doc):
    doc =json.loads(doc)
    if doc.get("room_no"):
       room_no=frappe.get_doc("Room HMS",doc.get("room_no"))
       room_no.status="Occupied"
       room_no.db_update()
       #room_no.save()

    
#function filtering all Room HMS on Basis Room Type on Room folio hms
#In Room No. Field      
@frappe.whitelist()
def room_no_fltr(doctype, txt, searchfield, start, page_len, filters):
    if txt:
       filters.update({"name": ("like", "{0}%".format(txt))})
    return frappe.get_all('Room HMS',filters=filters,fields=['name'],as_list=1)
       
    
