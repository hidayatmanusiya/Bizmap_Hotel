var room_ref_no =[]
var company =[]
frappe.ui.form.on('Sales Invoice', {
      
	refresh(frm) {

	if(frm.doc.room_folio_ref){
	  var Room_Folio = frm.doc.room_folio_ref
	  room_ref_no.push(Room_Folio)
	  frm.set_value("room_folio_ref","")
	  frm.set_value("room_folio",Room_Folio)
	  if(frm.docstatus=="Not Saved"){
          frm.set_value("room_folio_ref",Room_Folio)
         
          }
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
    	  
          frm.set_value('due_date',frappe.datetime.nowdate())
    	  frappe.call({
        method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.sales_order_item_transfer_to_sales_invoice',
        args:{
          'room_folio_ref':room_ref_no[0]
           },
        callback:function(r){
       frappe.db.get_value("Company",{"name":frm.doc.company},['default_income_account','default_expense_account'],(p) =>{
                 // company.push(p.default_income_account,p.default_expense_account)
                  //company.push()
                
                    //console.log([0]company)
                     //console.log([company])
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
		           childTable.sales_order=r.message[i][j][9]
		           //childTable.rate=r.message[i][j][7]
		           //childTable.amount= r.message[i][j][7] * r.message[i][j][8]
		           //childTable.base_rate=r.message[i][j][7]
		           //childTable.base_amount=r.message[i][j][7] * r.message[i][j][8]
		           //childTable.conversion_factor=r.message[i][j][5]
		           //childTable.item_tax_template=r.message[i][j][6]
		           //childTable.stock_qty=r.message[i][j][8]
		           //childTable.grant_commission=1
		           childTable.income_account = p.default_income_account
                           //childTable.expense_account=p.default_expense_account
                 }
                }
           })
            
          }
           
        }),
      
      frappe.call({
         method:'bizmap_hotel.bizmap_hotel.doctype.room_folio_hms.room_folio_hms.sales_order_sale_tax_to_sales_invoice_sale_tax',
       args:{
         'room_folio_ref':room_ref_no[0]
         },
        callback:function(r){
          console.log("--++--++",r)
          for (let i =0; i<r.message.length;i++) {
           for(let j=0; j<[i].length;j++){
            
            var childTable_taxes = cur_frm.add_child("taxes");
            childTable_taxes.charge_type= r.message[i][j].charge_type
            childTable_taxes.account_head= r.message[i][j].account_head 
            childTable_taxes.rate= r.message[i][j].rate
            
          }
         } 
        } 
      
      })  
        
    },
    onload:function(frm){
     if (frm.doc.selling_price_list == null){
        frm.set_value("selling_price_list","Standard Selling")
     }
    
    }
  	
})

