// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Rooms To Checkout"] = {
	"filters": [
              {
	          "label":"Check Out Date",
	          "fieldname":"check_out",
	          "fieldtype":"Date"
	          },
	          {
	           "label":"Status",
	           "fieldname":"status",
	           "fieldtype":"Select",
	           "options":["","Checked In","Checked Out"]
	          
	          }
	]
};
