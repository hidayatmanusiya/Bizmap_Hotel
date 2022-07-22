frappe.ui.form.on('Sales Order', {
    refresh:function(frm){
   
   frm.add_custom_button(__('Frondesk'), function(){
        //frappe.set_route(["query-report", "Gross Profit"]);
    })
    
     }
  }) 
