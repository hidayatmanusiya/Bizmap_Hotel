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
    }, __("Action")).css({'background-color': 'cyan','color':'black','border':'2px solid black'});;

  }	
	
		
    }
})
