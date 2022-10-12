frappe.listview_settings['Sales Order'] = {
    onload: function (listview) {
        listview.page.add_inner_button("Fetch Booking", function () {
            frappe.call({
                method: "bizmap_hotel.utill.booking.insertbooking",
                args: {}
            });
        });
    },
};