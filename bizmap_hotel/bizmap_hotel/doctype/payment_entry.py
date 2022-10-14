import frappe
from frappe.model.document import Document
import json



def before_submit(doc,method):
    frappe.reload_doctype("Room Folio HMS") 
    #frappe.reload_doctype("Collected  Payment")
    room_folio=frappe.db.get_value("Room Folio HMS",{"reservation":doc.room_folio_reference},"name")
    if room_folio:
       paymet_entry=frappe.db.sql(f""" select a.name,a.paid_amount,a.posting_date from `tabPayment Entry` as a inner join `tabPayment Entry Reference` as p on p.parent=a.name where p.reference_name="{doc.room_folio_reference}" """,as_dict=1)
       room_folio_payment=frappe.get_doc('Room Folio HMS',room_folio)
       room_folio_payment.collected_payment=[]
       for i in paymet_entry:
            payment_entry_child=room_folio_payment.append('collected_payment',{})
            payment_entry_child.voucher_type="Payment Entry"
            payment_entry_child.voucher=i.name
            payment_entry_child.date=i.posting_date
            payment_entry_child.amount=i.paid_amount
            #room_folio_payment.insert()
            room_folio_payment.run_method('submit')
            #room_folio_payment.reload()
            #frappe.reload_doctype("Collected  Payment")
            frappe.reload_doctype("Room Folio HMS")
       
       
       



       
       
       
       
       
    
        
