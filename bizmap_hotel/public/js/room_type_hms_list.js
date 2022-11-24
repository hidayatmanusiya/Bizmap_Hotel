frappe.listview_settings["Room Type HMS"] = {
	onload: function(listview) {
		update_channel_rooms(listview);
	},
	refresh: function(listview) {
		update_channel_rooms(listview);
	},
};

function update_channel_rooms(listview) {
	// eZee Booking Fetch Button
	frappe.db.get_single_value("Integration Settings", "ezee").then((val) => {
		if (val) {
			listview.page.add_inner_button("Update eZee Room", function() {
				frappe.call({
					method: "bizmap_hotel.utill.room.update_room",
					args: {},
				});
			});
		}
	});

	frappe.db.get_single_value("Integration Settings", "staah").then((val) => {
		if (val) {
			// STAHH Booking Fetch Button
			listview.page.add_inner_button("Update STAAH Room", function() {
				frappe.call({
					method: "bizmap_hotel.utill.room_staah.update_room",
					args: {},
				});
			});
		}
	});
}
