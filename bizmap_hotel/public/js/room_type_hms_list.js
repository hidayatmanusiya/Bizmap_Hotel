frappe.listview_settings["Room Type HMS"] = {
	onload: function(listview) {
		update_channel_rooms(listview);
	},
	refresh: function(listview) {
		update_channel_rooms(listview);
	},
};

function update_channel_rooms(listview) {
	frappe.call({
		method: "bizmap_hotel.utill.booking_staah.get_last_integration_setting",
		callback: function(r) {
			if (r.message.ezee) {
				listview.page.add_inner_button("Update eZee Room", function() {
					frappe.call({
						method: "bizmap_hotel.utill.room.update_room",
						args: {},
					});
				});
			}
			if (r.message.staah) {
				listview.page.add_inner_button("Update STAAH Room", function() {
					frappe.call({
						method: "bizmap_hotel.utill.room_staah.update_room",
						args: {},
					});
				});
			}
		},
	});
}
