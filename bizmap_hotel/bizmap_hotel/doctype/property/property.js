// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt

frappe.ui.form.on('Property', {
	 address: function(frm) {
           frappe.call({
              method:"bizmap_hotel.bizmap_hotel.doctype.property.property.get_adresss",
              args:{
               "doc":frm.doc
              },
              callback: function(r){
                frm.set_value("primary_address",r.message)
              }
           })
	 },
	
	 setup(frm){
    frm.set_query("contact", function() {
	return {
	query: 'bizmap_hotel.bizmap_hotel.doctype.property.property.contact_list',
	filters: {
	"address":frm.doc.address
		}
		}
	});
 },
 contact(frm){
    frappe.call({
              method:"bizmap_hotel.bizmap_hotel.doctype.property.property.get_mobile_emalil_frm_contact",
              args:{
               "doc":frm.doc
              },
              callback: function(r){
                frm.set_value("moblle_no",r.message[0])
                frm.set_value("email_id",r.message[1])
              }
           })
 
 
 }
 
});
