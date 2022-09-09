let _bryntum$scheduler = bryntum.scheduler,
    Scheduler = _bryntum$scheduler.Scheduler,
    ResourceStore = _bryntum$scheduler.ResourceStore,
    EventStore = _bryntum$scheduler.EventStore,
    DateHelper = _bryntum$scheduler.DateHelper,
    AjaxHelper = _bryntum$scheduler.AjaxHelper,
    StringHelper = _bryntum$scheduler.StringHelper;

let schedule;
schedule = new Scheduler({
    ref: 'schedule',
    id: 'container_frontdesk',
    insertFirst: 'main',
    features: {
        // eventDragCreate: false,
        eventResize: false,
        eventTooltip: false,
        stickyEvents: false,
        eventDrag: {
            disabled: true
        },
        group: 'room_type_name',
        eventEdit: {
            editorConfig: {
                title: "New Booking",
                // bbar: {
                //     items: [
                //         {
                //             reference: 'saveButton',
                //             backGround: 'green',
                //             text: 'Save',
                //             handler: 'saveTask',
                //             onClick({ source: combo }) {
                //                 console.log(combo)
                //             },
                //         },
                //     ]
                // },
            },
            // Add extra widgets to the event editor
            items: {
                nameField: null,
                resourceField: null,
                startDateField: {
                    label: 'Check In'
                },
                endDateField: {
                    label: 'Check Out'
                },
                customerCombo: {
                    type: 'combo',
                    ref: 'customerCombo',
                    // store: data.customers.rows,
                    name: 'customer',
                    label: 'Customer',
                    placeholder: 'Select customer...',
                    weight: 130,
                    clearable: true,
                },
                companyCombo: {
                    type: 'combo',
                    ref: 'companyCombo',
                    // store: data.companys.rows,
                    name: 'company',
                    label: 'Company',
                    placeholder: 'Select Company...',
                    weight: 130,
                    clearable: true,
                },
                roomTypeCombo: {
                    type: 'combo',
                    ref: 'roomTypeCombo',
                    // store: data.roomTypes.rows,
                    name: 'room_type',
                    label: 'Room Type',
                    placeholder: 'Select Room Type...',
                    weight: 130,
                    clearable: true,
                },
                roomNoCombo: {
                    type: 'combo',
                    ref: 'roomNoCombo',
                    // store: data.rooms.rows,
                    name: 'room_no',
                    label: 'Room No',
                    placeholder: 'Select Room No...',
                    weight: 130,
                    clearable: true,
                },
                packageCombo: {
                    type: 'combo',
                    ref: 'packageCombo',
                    // store: data.items.rows,
                    name: 'room_package',
                    label: 'Room Package',
                    placeholder: 'Select Package No...',
                    weight: 130,
                    clearable: true,
                },
            }
        },

    },
    columns: [
        {
            text: 'status', field: 'status', width: 20, region: 'left',
            htmlEncode: false,
            editor: null,
            renderer({ value }) {
                return `<div class="capacity b-fa b-fa-${statusObj[value]}"></div>`;
            }
        },
        { text: '', editor: null, sort: null, field: 'room_type', width: 100, region: 'left' },
        { text: 'Room No', editor: null, field: 'room_no', width: 100, region: 'left' },
    ],

    rowHeight: 40,
    // startDate: new Date(2017, 5, 1),
    // endDate: new Date(2017, 5, 11),
    viewPreset: {
        base: 'dayAndWeek',
        headers: [
            {
                unit: 'day',
                align: 'center',
                renderer: (startDate, endDate) => `
                    <div>${DateHelper.format(startDate, 'ddd')}</div>
                    <div>${DateHelper.format(startDate, 'DD MMM')}</div>
                `
            }
        ]
    },
    eventLayout: 'none',
    managedEventSizing: false,

    crudManager: {
        autoLoad: true,
        resourceStore: new ResourceStore({
            // data: data.resources.rows
        }),
        eventStore: new EventStore({
            // data: data.events.rows,
        })
    },

    eventRenderer({ eventRecord, resourceRecord, renderData }) {
        let startEndMarkers = '';
        renderData.cls[eventRecord.status] = 1;

        // if (eventRecord.status) {
        //     startEndMarkers = `<i class="b-start-marker ${eventRecord.startInfoIcon}" data-btip="${eventRecord.startInfo}"></i>`;
        // }
        // if (eventRecord.workflow_state) {
        //     startEndMarkers += `<i class="b-end-marker ${eventRecord.endInfoIcon}" data-btip="${eventRecord.endInfo}"></i>`;
        // }

        return startEndMarkers + StringHelper.encodeHtml(eventRecord.customer);
    },

    tbar: [
        {
            type: 'DateField',
            ref: 'startDate',
            name: 'start_date',
            weight: 50,
            placeholder: 'Start Date',
            clearable: true,
        },
        {
            type: 'DateField',
            ref: 'endDate',
            name: 'end_date',
            weight: 50,
            placeholder: 'End Date',
            clearable: true,
        },
        {
            type: 'combo',
            ref: 'companyCombo',
            // store: data.companys.rows,
            store: ['Bizmap Hotel'],
            name: 'companys',
            placeholder: 'Company...',
            weight: 50,
            multiSelect: true,
            clearable: true,
            listeners: {
                async change({ value }) {
                    // Property
                    let filters = []
                    for (let item of value) {
                        filters.push(["Property", "company", "=", item])
                    }
                    let propertyParams = `doctype=Property&cmd=frappe.client.get_list&fields=${JSON.stringify(["*"])}&filters=${JSON.stringify(filters)}&limit_page_length=None`;
                    let propertyArray = await apiPostCall('/', propertyParams, window.frappe?.csrf_token)
                    for (let item of propertyArray) {
                        item.id = item.name
                        item.text = item.name
                    }
                    // propertys = propertyArray
                }
            }
        },
        {
            type: 'combo',
            ref: 'propertieCombo',
            // store: propertys,
            name: 'properties',
            weight: 50,
            placeholder: 'Propertie...',
            clearable: true,
            listeners: {
                change({ value }) {
                    let schedule = window.bryntum.get('scheduler');
                    console.log(value)
                    console.log(schedule.propertys)
                    // scheduler.refreshWithTransition();
                }
            }
        },
        {
            type: 'combo',
            ref: 'statuseCombo',
            // store: data.status.rows,
            name: 'status',
            weight: 50,
            placeholder: 'Status...',
            clearable: true,
            listeners: {
                change({ value }) {
                    console.log(value)
                    // scheduler.refreshWithTransition();
                }
            }
        }
    ]
});