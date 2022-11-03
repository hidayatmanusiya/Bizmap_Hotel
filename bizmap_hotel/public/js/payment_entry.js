var room_folio_ref=[]
var Amount =[]
frappe.ui.form.on('Payment Entry', {
onload(frm) {
    if(frm.doc.room_folio_reference){
             frappe.call({
                   method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.payment_entry',
                   args:{
                   'doc':frm.doc,
                  },
                 callback:function(r){
                      if(r.message){
                         frm.set_value("contact_person",r.message[0][2])    
                         frm.set_value("party",r.message[0][1])
                         Amount.push(r.message[0][3])
                     setTimeout(()=>{
                        if(frm.doc.paid_amount==null){
                          frm.set_value("paid_amount",r.message[0][3])
                        }
                     },1000);
                 }
              }
         })
     }     	
},
paid_amount(frm){
     //cur_frm.get_field("references").grid.grid_rows[0].remove();
     
    var tbl = frm.doc.references || [];
    var i = tbl.length;
       //while (i--) {
      //  if(frm.doc.items[i].idx == 0) {
        //    cur_frm.get_field("references").grid.grid_rows[i].remove();
          //  frm.refresh_field("references")
       // }
   // }
        cur_frm.refresh();
        var Refchild=cur_frm.add_child("references")
        Refchild.reference_doctype="Sales Order"
        Refchild.reference_name=frm.doc.room_folio_reference
        Refchild.total_amount = Amount[0]
        Refchild.outstanding_amount= Amount[0]
        Refchild.allocated_amount=Amount[0]

},
before_save(frm){
   frappe.call({
      method:"bizmap_hotel.bizmap_hotel.doctype.payment_entry.payment_entry_in_collection_pymt_room_folio",
      args:{
        'doc':frm.doc,
      }
   })
  }
  
  
	
})
