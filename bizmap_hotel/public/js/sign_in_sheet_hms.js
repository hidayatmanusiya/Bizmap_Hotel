// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Sign In Sheet HMS', {
// 	// refresh: function(frm) {

// 	// }
// });

frappe.ui.form.on("Sign In Sheet HMS", {
    refresh: function(frm) {
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

    }
});