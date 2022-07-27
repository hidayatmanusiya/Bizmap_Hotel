frappe.ui.form.on('Room Folio HMS', {
	refresh:function(frm) {
		frm.add_custom_button(__('Frondesk'), function(){
        //frappe.set_route(["query-report", "Gross Profit"]);
        
    })
    if(frm.doc.docstatus==1){
         cur_frm.add_custom_button(__('Make Pyment'), function(){
         
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
    
    frm.add_custom_button(__('Make Sign In sheet'), function(){
    
       frappe.model.open_mapped_doc({
	      method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.map_sign_in_sheet_with_room_folio',
	        frm:cur_frm
	    });     
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
    
        frm.add_custom_button(__('Sales Invoice'), function(){
    
       frappe.model.open_mapped_doc({
	      method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.room_folio_sales_invoice',
	        frm:cur_frm
	    });     
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});
    

  }	
	
		
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
