// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Folio HMS', {
	refresh: function(frm) {
		frm.add_custom_button(__("Sales Order"), function() {
			var so_list = [];
			frappe.call({
				method:"bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.get_sales_order",
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
						        $.each(selections, function(idx, val){
						        	var d = frm.add_child("sales_book_item");
								    d.sales_order= val
						        	frappe.call({
										method: "frappe.client.get",
										args: {
											doctype: "Sales Order",
											filters: {name: val}
										},
										callback: function(r) {
											if(r.message){
										        d.date = r.message.transaction_date
										        d.description = r.message.status
										        d.amount = r.message.grand_total
										        refresh_field("date", d.name, d.parentfield);
												refresh_field("description", d.name, d.parentfield);
												refresh_field("amount", d.name, d.parentfield);
											}
										}
									});
							    });
							    frm.refresh_field("sales_book_item");
							    $(".modal").modal("hide");
						    }
						});
                    }
				}
            });
        });

	}
});



		
