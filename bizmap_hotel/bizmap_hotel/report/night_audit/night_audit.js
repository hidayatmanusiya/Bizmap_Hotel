// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Night Audit"] = {
	"filters": [
                 {
	          "label":"Date",
	          "fieldname":"date",
	          "fieldtype":"Date"
	          },
	          {
	           "label":"Operation",
	           "fieldname":"operation",
	           "fieldtype":"Select",
	           "options":["","Rooms to Charge","Rooms to Checkin","Rooms to Chckout"]
	          
	          }
	]
};
