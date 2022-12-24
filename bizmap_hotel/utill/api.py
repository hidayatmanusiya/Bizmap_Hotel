import frappe


@frappe.whitelist()
def fetch_data(from_date, to_date):
	data = []
	companies = frappe.get_all("Company", fields=['name', 'abbr'])
	for company in companies:
		company_data = {}
		# build company_data for each individual company
		company_data["company_name"] = company.name
		company_data["company_abbreviation"] = company.abbr or ""
		properties = frappe.get_all("Property", filters={"company": company.name}, fields=['name', 'property_abbreviation'])
		for property in properties:
			room_types = frappe.db.sql(f"""select a.name, a.room_type_abbr from `tabRoom Type HMS` a inner join `tabProperty Child table` c on c.parent=a.name where c.property_name= "{property.name}" """, as_dict=1)
			if room_types:
				company_data["properties"] = {}
				company_data["properties"][property["name"]] = {"Property_abbreviation": property.property_abbreviation or ""}
				company_data["properties"][property["name"]]["RoomType"] = {}
				for room_type in room_types:
					rooms = frappe.get_all("Room HMS", filters={"room_type": room_type.name}, fields=['name', 'status', 'non_smoking', 'bed_type'])
					if rooms:
						company_data["properties"][property["name"]]["RoomType"][room_type.name] = {"Room_abbreviation": room_type.room_type_abbr or "", "RoomNumbers": {}}
						for room in rooms:
							company_data["properties"][property["name"]]["RoomType"][room_type.name]["RoomNumbers"][room.name] = {
								"CurrentStatus": room.status or "",
								"NonSmoking": room.non_smoking or "",
								"BedType": room.bed_type or "",
								"RoomLedger": []
							}
							q = f"""select name, room, room_type, from_date, to_date, record_type, booking_type, note from `tabRoom Balance Ledger` where from_date between "{from_date}" and "{to_date}" or  to_date between "{from_date}" and "{to_date}" """
							ledgers = frappe.db.sql(q, as_dict=1)
							for ledger in ledgers:
								company_data["properties"][property["name"]]["RoomType"][room_type.name]["RoomNumbers"][room.name]["RoomLedger"].append({
									"From": ledger.from_date.strftime("%d/%m/%Y"),
									"to": ledger.to_date.strftime("%d/%m/%Y"),
									"BookingType": ledger.booking_type or "",
									"BookingCategory": ledger.booking_type or ""
								})


		# add company_data to data
		data.append(company_data)
	return data


@frappe.whitelist()
def get_rooms(from_date, to_date, room_type=None, booking_from=None, booking_to=None, booking_type=None, status=None):
	# considering date is in the form ~ "2022-12-09"
	q = f"""select name, room, room_type, from_date, to_date, record_type, booking_type, note from `tabRoom Balance Ledger` where from_date between "{from_date}" and "{to_date}" or  to_date between "{from_date}" and "{to_date}")"""
	ledger = frappe.db.sql(q, as_dict=1)
	data = {}
	for l in ledger:
		if l["room_type"] not in data:
			data[l["room_type"]] = []
	for l in ledger:
		data[l["room_type"]].append(l)
	return data


@frappe.whitelist()
def get_number_of_available_rooms(from_date, to_date, room_type, room=None, property=None, company=None):
	# Expecting dates in the format - '2022-12-03' ~ %Y%m%d
	if room:
		ledgers = frappe.db.sql(f"""select name from `tabRoom Balance Ledger` where room= "{room}" and (from_date between "{from_date}" and "{to_date}" or  to_date between "{from_date}" and "{to_date}")""")
		if ledgers:
			# Room not available
			return 0
		else:
			return 1
	elif room_type:
		data = {}
		room_filters = {"room_type": room_type}
		if company:
			room_filters["company"] = company
		if property:
			room_filters["property"] = property
		total_rooms = frappe.get_all("Room HMS", filters=room_filters)
		total_rooms = [room['name'] for room in total_rooms]
		number_of_total_rooms = len(total_rooms)
		q = f"""select room from `tabRoom Balance Ledger` where room_type= "{room_type}" and
		(from_date between "{from_date}" and "{to_date}" or  to_date between "{from_date}" and "{to_date}")
		group by "room" """
		booked_rooms = [r[0] for r in frappe.db.sql(q)]
		number_of_available_rooms = number_of_total_rooms - len(booked_rooms)
		for booked_room in booked_rooms:
			total_rooms.remove(booked_room)
		data[number_of_available_rooms] = total_rooms
		return data


def create_ledger(doc, method):
	if doc.doctype == "Sales Order":
		ledger = frappe.get_doc({
			"doctype": "Room Balance Ledger",
			"from_date": doc.check_in_cf,
			"to_date": doc.check_out_cf,
			"room_type": doc.room_type_cf,
			"reference": doc.name,
			"room": doc.get('room_no'),
			"booking_type": doc.get('booking_type'),
			"record_type": "IN"
		})
		ledger.save()

	if doc.doctype == "Room Folio HMS" and doc.status == "Checked Out":
		ledger = frappe.get_doc({
			"doctype": "Room Balance Ledger",
			"from_date": doc.check_in,
			"to_date": doc.check_out,
			"folio_reference": doc.name,
			"room": doc.get('room_no'),
			"record_type": "OUT",
			"room_type": doc.room_type,

		})
		ledger.save()
