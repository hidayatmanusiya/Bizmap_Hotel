var room_ref_no =[]
frappe.ui.form.on('Sales Invoice', {
      
	refresh(frm) {
	if(frm.doc.room_folio_ref){
	  var Room_Folio = frm.doc.room_folio_ref
	  room_ref_no.push(Room_Folio)
	  frm.set_value("room_folio_ref","") 
          frm.set_value("room_folio_ref",Room_Folio)
          frappe.call({
        method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.sales_order_item_transfer_to_sales_invoice',
        args:{
          'room_folio_ref':frm.doc.room_folio_ref
           },
        callback:function(r){
          
          }
            })
          }
	},
    	room_folio_ref(frm){
    	  frappe.call({
        method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.sales_order_item_transfer_to_sales_invoice',
        args:{
          'room_folio_ref':room_ref_no[0]
           },
        callback:function(r){
                    //cur_frm.get_field("items").grid.grid_rows[1].remove();
                    //cur_frm.refresh("items");
                    console.log(r)
                    cur_frm.clear_table("items");
                for (let i =0; i<r.message.length;i++) {
                    for(let j=0; j<[i].length;j++){
                          var childTable = cur_frm.add_child("items")
                          //cur_frm.refresh_fields("items")
		           childTable.item_code = r.message[i][j][0]
		           childTable.item_name=r.message[i][j][3]
		           childTable.description=r.message[i][j][2]
		           childTable.uom=r.message[i][j][1]
		           childTable.qty =r.message[i][j][8]
		           childTable.conversion_factor=r.message[i][j][5]
		           childTable.item_tax_template=r.message[i][j][6]
		           //childTable.stock_qty=2
                    
                 }
                }
            
            
          }
        })
    	}
  	
})

