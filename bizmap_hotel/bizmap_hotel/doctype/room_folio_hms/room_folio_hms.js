// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Folio HMS', {
	refresh: function(frm) {
	      if(frm.doc.docstatus==1){
		frm.add_custom_button(__("Sales Order"), function() {
			var so_list = [];
			frappe.call({
				method:"bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.get_sales_order",
				args:{
				 "doc":frm.doc
				},
				callback: function(r) {
					$.each(r.message, function(idx, val){
				        if (val) so_list.push(val);
				    });
				    if (so_list.length > 0){
			            new frappe.ui.form.MultiSelectDialog({
						    doctype: "Sales Order",
						    target: cur_frm,
						    setters: {
						        //status: 'Pending'
						    },
						    primary_action_label:__("Get Data"),
						    get_query: function () {
								return {
		                			filters:{"name":['in', so_list]}
								}
							},
						    action(selections) {
						        //console.log("selections",selections)
						         
						    let sales_invoice = frappe.model.get_new_doc('Sales Invoice')
						        
						         sales_invoice.naming_series="SINV-.YY.-"
						         sales_invoice.company=frm.doc.company
						         sales_invoice.customer=frm.doc.customer
						         sales_invoice.posting_date=frappe.datetime.nowdate()
						         //sales_invoice.selling_price_list="Standard Selling"
						    setTimeout(()=>{
                                                     frappe.set_route("Form", sales_invoice.doctype, sales_invoice.name)
                                                    },3000)    
			                                
frappe.db.get_value("Company",{"name":frm.doc.company},['default_income_account','default_expense_account','cost_center'],(p) =>{       
						     for (let i =0; i<selections.length;i++){
				                      frappe.model.with_doc("Sales Order",selections[i],function(){
                                                     var itemschild_data = frappe.model.get_doc("Sales Order",selections[i])
                                                      if(itemschild_data.items){
	                                                frm.clear_table('items');
	                                                 $.each(itemschild_data.items,
	                                                 function(index,row){
	                                                 var detail = frappe.model.get_new_doc("Sales Invoice Item",sales_invoice,"items");
	                                   
	                                               $.extend(detail, {
                                                      "item_code":row.item_code,
                                                      "item_name":row.item_name,
                                                      "description":row.description,
                                                      "uom":row.uom,
                                                      "qty":row.qty,
                                                      "sales_order":selections[i],
                                                      "income_account" : p.default_income_account,
                                                      "cost_center" :p.cost_center
                                                       });
	                                        })
	   
                                           }

                                     })
                                     
                                     //---- for insert selected sales order in table 
           let value = frappe.db.get_value('Sales Order',{'name':selections[i]},['transaction_date','grand_total'],(r) =>{  
                         frappe.call({
                             method: 'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.description_for_sales_books',
                            args: {
                            name:selections[i]
                             },
	                   async: false,
                         callback: function(p) {
                         var childTable_so_itm = cur_frm.add_child("sales_book_item")
                             childTable_so_itm.sales_order=selections[i]
                             childTable_so_itm.date=r.transaction_date
                             childTable_so_itm.amount=r.grand_total
                             childTable_so_itm.description= p.message[0].description
                             
                             
                             }
                              
                          });
                          
                            setTimeout(() => {
                               frm.save('Update')
                            }, 100)
                                   
                                     })
                             //---------
                              
			 }
			 
		     })								
									
							    
							      
							    $(".modal").modal("hide");
						    }
						});
                    }
				}
            });
        });

	}
      }	
});

