frappe.listview_settings['Room Type HMS'] = {
    onload: function (listview) {
        // eZee Booking Fetch Button
        listview.page.add_inner_button("Update eZee Room", function () {
            frappe.call({
                method: "bizmap_hotel.utill.room.update_room",
                args: {}
            });
        });
        // STAHH Booking Fetch Button
        listview.page.add_inner_button("Update STAAH Room", function () {
            frappe.call({
                method: "bizmap_hotel.utill.room_staah.update_room",
                args: {}
            });
        });
    },
};

