frappe.listview_settings['Sales Order'] = {
    onload: function (listview) {
        // eZee Booking Fetch Button
        listview.page.add_inner_button("Fetch Booking", function () {
            frappe.call({
                method: "bizmap_hotel.utill.booking.insertbooking",
                args: {}
            });
        });
        // STAHH Booking Fetch Button
        listview.page.add_inner_button("STAAH Booking", function () {
            frappe.call({
                method: "bizmap_hotel.utill.booking_staah.insertbooking",
                args: {}
            });
        });
    },
};

