frappe.listview_settings["Sales Order"] = {
	onload: function(listview) {
		fetch_bookings(listview);
	},
	refresh: function(listview) {
		fetch_bookings(listview);
	},
};

function fetch_bookings(listview) {
	// eZee Booking Fetch Button
	frappe.db.get_single_value("Integration Settings", "ezee").then((val) => {
		if (val) {
			listview.page.add_inner_button("Fetch Booking", function() {
				frappe.call({
					method: "bizmap_hotel.utill.booking.insertbooking",
					args: {},
				});
			});
		}
	});
	// STAHH Booking Fetch Button
	frappe.db.get_single_value("Integration Settings", "staah").then((val) => {
		if (val) {
			listview.page.add_inner_button("STAAH Booking", function() {
				frappe.call({
					method: "bizmap_hotel.utill.booking_staah.insertbooking",
					args: {},
				});
			});
		}
	});
}
