frappe.ui.form.on('Room Folio HMS', {
	refresh:function(frm) {
	frm.add_custom_button(__('Frondesk'), function(){
        //frappe.set_route(["query-report", "Gross Profit"]);
        
    })
    if(frm.doc.docstatus==1){
         cur_frm.add_custom_button(__('Make Pyment'), function(){
              let payment = frappe.model.get_new_doc('Payment Entry')
              payment.naming_series='ACC-PAY-.YYYY.-'
              payment.payment_type='Receive'
              payment.party_type='Customer'
              payment.posting_date=frappe.datetime.nowdate()
              payment.room_folio_reference=frm.doc.reservation
             // payment.company=frm.doc.company
              frappe.db.get_list('Company', {
            fields: ['default_bank_account'],
            filters: {
                'name': frm.doc.company
            }
        }).then(function(Default_Bank) {
            payment.paid_to=Default_Bank[0].default_bank_account
            //frm.set_value("paid_to", );
        });
              frappe.set_route("Form", payment.doctype, payment.name);
            
              
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
   } 
    if(frm.doc.sign_in_sheet==null && frm.doc.docstatus==0){ 
    frm.add_custom_button(__('Make Sign In sheet'), function(){
          let lcv = frappe.model.get_new_doc('Sign In Sheet HMS');
          lcv.room_folio = cur_frm.doc.name;
          frappe.set_route("Form", lcv.doctype, lcv.name);
            
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
   } 
   if(frm.doc.docstatus==1){
        frm.add_custom_button(__('Sales Invoice'), function(){
        var sales_invoice =frappe.db.get_value("Sales Invoice",{'room_folio':frm.doc.name},'room_folio',(r) => {
        if(frm.doc.name!=r.room_folio){
       frappe.model.open_mapped_doc({
	      method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.room_folio_sales_invoice',
	        frm:cur_frm
	    });    
	  }
	   else{
	       frappe.throw(__("Sales Invoice for Room Folio '{0}' is alrady existing  ",[frm.doc.name]))
	   } 
	  })   
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
  }  
    if(frm.doc.docstatus==1 && frm.doc.status=="Pre-Check In"){
    frm.add_custom_button(__('Check-In'), function(){
        frappe.call({
         method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.check_in_button',
         args:{
          'doc':frm.doc
         }
        
        })
     },__("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
 } 	
  if(frm.doc.docstatus==1 && frm.doc.status=="Checked In"){
        frm.add_custom_button(__('Check-Out'), function(){
        frappe.call({
          method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.check_out_button',
          args:{
           'doc':frm.doc
           }
         })
    
     },__("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});	
  }		
    },
    check_out(frm){
       
           frappe.call({
    method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.checkout_minus_checkin_days_diffrence',
    args: {
        'doc':frm.doc
    },
	async: false,
    callback: function(r) {
        
          frm.set_value("quantity",r.message)
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
    callback: function(r) {
       // console.log(r.message[0].description)
          frappe.model.set_value(cdt,cdn,'description',r.message[0].description)
    }
});

 
    
})


//frappe.ui.form.on('Room Folio HMS', "refresh", function(frm) {
 //   frm.add_custom_button(__("Sign In Sheet HMS"), function() {


   // });
//});



