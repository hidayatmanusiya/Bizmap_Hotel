frappe.listview_settings['Room Folio HMS'] = {
    
    get_indicator: function(doc){
        const status_color = {
                "Checked Out":"green",
                "Pre-Check In":"gray",
                "Checked In":"yellow"

            };
        
         if(doc.status==="Checked In"){
            return [__(doc.status),status_color[doc.status]]
        }
        if(doc.status==="Checked Out"){
            
            return [__(doc.status),status_color[doc.status]]
        }
        if(doc.status==="Pre-Check In"){
            return [__(doc.status),status_color[doc.status]]
        }
       
        if(doc.status==="Skipper"){
            return [__(doc.status),status_color[doc.status]]
        }
        
    }
}

