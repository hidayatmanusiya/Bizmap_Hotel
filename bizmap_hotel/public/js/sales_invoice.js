
frappe.ui.form.on('Sales Invoice', {
	refresh(frm) {
	},

    onload:function(frm){
     if (frm.doc.selling_price_list == null){
        frm.set_value("selling_price_list","Standard Selling")
     }
    
    }
  	
})

