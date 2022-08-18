// Copyright (c) 2022, BizMap and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Room Occupancy and Revenue HMS"] = {
	"filters": [
	          {
	          "label":"from date",
	          "fieldname":"from_date",
	          "fieldtype":"Date"
	          },
	          {
	          "label":"to date",
	          "fieldname":"to_date",
	          "fieldtype":"Date"
	          },
                  {
                  
                  
                  "label":"Company",
		   "fieldname":"company",
		   "fieldtype":"Link",
		   "options":"Company"
                  
                  
                  }
	]
};
