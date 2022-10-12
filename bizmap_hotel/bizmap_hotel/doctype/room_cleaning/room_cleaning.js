// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Cleaning', {
	// refresh: function(frm) {

	// }
	
	
setup(frm){
    frm.set_query("room_no", function() {
	return {
	query: 'bizmap_hotel.bizmap_hotel.doctype.room_cleaning.room_cleaning.room_no_fltr',
	filters: {
	"room_type":frm.doc.room_type
		}
		}
	});
 }
 
	
});
