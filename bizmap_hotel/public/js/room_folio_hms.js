frappe.ui.form.on('Room Folio HMS', {
	refresh:function(frm) {	
	frm.add_custom_button(__('Frondesk'), function(){
        
    })
    
    if(frm.doc.docstatus==1){
              cur_frm.add_custom_button(__('Make Pyment'), function(){
              
              
                frappe.call({ 
                  method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.payment_entry_from_room_folio',
                  args:{
                     'doc':frm.doc,
                  },
                 callback:function(r){
                   console.log(r)
                   if(r.message){
                    frappe.set_route("Form", "Payment Entry",r.message)
                   }
                 } 
                })
              
   }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
} 
  if(frm.doc.sign_in_sheet==null && frm.doc.docstatus==1 && frm.doc.status=="Pre-Check In" ){ 
               frm.add_custom_button(__('Make Sign In sheet'), function(){
                   let lcv = frappe.model.get_new_doc('Sign In Sheet HMS');
                   lcv.room_folio = cur_frm.doc.name;
                   lcv.customer_email=cur_frm.doc.customer_email;
                   lcv.customer_mobile=cur_frm.doc.customer_mobile;
               frappe.set_route("Form", lcv.doctype, lcv.name);
            
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
 } 
  if(frm.doc.docstatus==1 && frm.doc.status=="Checked In"){
           frm.add_custom_button(__('Sales Invoice'), function(){
           sales_invoice =frappe.db.get_value("Sales Invoice",{'room_folio':frm.doc.name},'room_folio',(r) => {
           if(frm.doc.name!=r.room_folio){
              frappe.call({
      method:"bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.sales_order_item_transfer_to_sales_invoice" ,
       args :{
          "doc":frm.doc
           },
      callback:function(r){
           if(r.message){
             frappe.set_route("Form", "Sales Invoice",r.message)
                 }
                }     
              })
            }
           else{
              frappe.throw(__("Sales Invoice for Room Folio '{0}' is alrady existing  ",[frm.doc.name]))
            } 
          }) 
               
      }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
   }  
 if(frm.doc.docstatus==1 && frm.doc.status=="Pre-Check In"){
                 frm.add_custom_button(__('Check-In'), function(){
                 frm.set_value("status","Checked In")
                 frm.save('Update')
                 frm.refresh(); 
                 frappe.call({
                        method:"bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.room_master_status",
                        args:{
                            "doc":frm.doc
                          }
        
                      })
         },__("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});     
 } 	
  if(frm.doc.docstatus==1 && frm.doc.status=="Checked In"){
         frm.add_custom_button(__('Check-Out'), function(){
         frm.set_value("status","Checked Out")
         frm.set_value("check_out",frappe.datetime.now_datetime())
         frm.save('Update')
         frm.refresh();
         frappe.call({
                method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.room_cleanig_doc',
                args: {
                  'doc':frm.doc
                 },
                 callback: function(r){
                       frappe.set_route("Form", "Room Cleaning",r.message)
                   }
            });
          },__("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});	
  }
      total_charges(frm)
      advance_against_reservation(frm)
      outstanding_charges(frm)		
    },
check_out(frm){
    frappe.call({
          method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.checkout_minus_checkin_days_diffrence',
          args: {
           'doc':frm.doc
          },
	async: false,
       callback: function(r){
           if(r.message){     
             frm.set_value("quantity",r.message)
            } 
        }
    });
},
 after_save(frm){
   if(frm.doc.sign_in_sheet==null){
     frm.set_intro("");
     frm.set_intro(__("Submit this document to continue with the flow."), true);
    } 
 },
 before_submit(frm){
 
   frm.set_value("status","Pre-Check In")
 
 },
 onload:function(frm){
     let value = frappe.db.get_value('Sales Order',{'name':frm.doc.reservation},['transaction_date','grand_total'],(r) =>{
         if (frm.doc.reservation!=null){
            frappe.call({
                  method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.description_for_sales_books',
                  args: {
                  name:frm.doc.reservation
                  },
	        async: false,
               callback: function(p) {
                  if (frm.doc.room_no==null){
                      var childTable_so_itm = cur_frm.add_child("sales_book_item")
                      childTable_so_itm.sales_order=frm.doc.reservation
                      childTable_so_itm.date=r.transaction_date
                      if(p.message[0]){
                          childTable_so_itm.description= p.message[0].description
                        }
                      childTable_so_itm.amount=r.grand_total
                      cur_frm.refresh();
                  }
               } 
           });
        }    
  })
   
   
 let guest_tbl = frappe.db.get_value('Sales Order',{'name':frm.doc.reservation},['guest_cf','guest_first_name','guest_last_name','contact_mobile','contact_email'],(r) =>{
     if (frm.doc.room_no==null){
            var childTable_guest_tbl = cur_frm.add_child("room_guest_detail")
            childTable_guest_tbl.guest=r.guest_cf
            childTable_guest_tbl.first_name=r.guest_first_name
            childTable_guest_tbl.last_name= r.guest_last_name
            childTable_guest_tbl.mobile=r.contact_mobile
            childTable_guest_tbl.email=r.contact_email
            cur_frm.refresh();
     }
   })
 },
 setup(frm){
      frm.set_query("room_no", function() {
	  return {
	    query: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.room_no_fltr',
	    filters: {
	         "room_type":frm.doc.room_type,
	         "property": frm.doc.property
            }
	}
    });
    
    frm.set_query("room_type", function() {
	  return {
	    query: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.room_type_fltr',
	    filters: {

	         "property": frm.doc.property
            }
	}
    });
 }

})

frappe.ui.form.on('Sales Book Item',"sales_order",function(frm,cdt,cdn){
var d =locals[cdt][cdn]
    frappe.call({
          method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.description_for_sales_books',
          args: {
            name:d.sales_order
        },
	async: false,
        callback: function(r){
          if(r.message[0]){
            frappe.model.set_value(cdt,cdn,'description',r.message[0].description)
          }
       }
   });
})

function total_charges(frm){
      var sales_book_itm= frm.doc.sales_book_item
      var amount =0
      for(let i in sales_book_itm) {
      const iterator =  sales_book_itm[i]
      amount = amount + iterator.amount
      }
     frm.set_value("total_charges",amount)

}
function advance_against_reservation(frm){

     var collected_payment = frm.doc.collected_payment
     var collected_amount = 0
     for(let i in collected_payment){
       const iterator =collected_payment[i]
       collected_amount = collected_amount + iterator.amount
   }
   frm.set_value("total_advance_paid",collected_amount)
}

function outstanding_charges(frm){
 if(frm.doc.total_charges && frm.doc.total_advance_paid){
     var outstanding_charges = frm.doc.total_charges -frm.doc.total_advance_paid
     frm.set_value("outstanding_charges",outstanding_charges)
    }
}
