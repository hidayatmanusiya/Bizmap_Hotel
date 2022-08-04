// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Sign In Sheet HMS', {
// 	// refresh: function(frm) {

// 	// }
// });

frappe.ui.form.on("Sign In Sheet HMS", {
    refresh: function(frm) {
      frm.add_custom_button(__('Room Folio'), function(){
        var back_to_room_folio=frappe.db.get_value("Room Folio HMS",{'sign_in_sheet':frm.doc.name},'name',(r) => {
        if(r.name!=null){
             frappe.set_route("Form", "Room Folio HMS",r.name)
           }
        })
      });
    
        if (cur_frm.doc.room_folio != null) {
            cur_frm.trigger("room_folio");
        }

    },
    room_folio: function(frm) {
        frappe.db.get_list('Room Guest Detail HMS', {
            fields: ['guest'],
            filters: {
                'parent': frm.doc.room_folio
            }
        }).then(function(doc) {
            // console.log(doc);
            cur_frm.set_value("guest", doc[0].guest);
        });

    },
    validate(frm){
      var back_to_room_folio=frappe.db.get_value("Room Folio HMS",{'name':frm.doc.room_folio},'sign_in_sheet',(r) => {
      if(r.sign_in_sheet!=null){
       
        frappe.throw(__("Sing Sheet for Room Folio '{0}' is alrady Existing  ",[frm.doc.room_folio]))
         frm.set_value("room_folio","")
              }
      else{
        frappe.call({
        method:'bizmap_hotel.bizmap_hotel.doctype.sign_in_sheet_hms.sign_in_sheet_hms.fill_sign_sheet_name_to_room_folio',
        args:{
             'doc':frm.doc
            }
        })
           
      }
   })

  }
});
