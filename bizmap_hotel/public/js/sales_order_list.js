frappe.listview_settings["Sales Order"] = {
	onload: function(listview) {
		console.log('onload');
		fetch_bookings(listview);
	}
};

function fetch_bookings(listview) {
	frappe.call({
		method:"bizmap_hotel.utill.booking_staah.get_last_integration_setting",
		callback: function(r){
			if (r.message.ezee){
				listview.page.add_inner_button("Fetch Booking", function() {
					frappe.call({
						method: "bizmap_hotel.utill.booking.insertbooking",
						args: {},
					});
				});
			}
			if (r.message.staah){
				listview.page.add_inner_button("STAAH Booking", function() {
					frappe.call({
						method: "bizmap_hotel.utill.booking_staah.insertbooking",
						args: {},
					});
				});
			}
		}
	 })
}
