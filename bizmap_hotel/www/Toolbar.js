let _bryntum$scheduler = bryntum.scheduler,
   WidgetHelper = _bryntum$scheduler.WidgetHelper;




// import SharedToolbar from "./SharedToolbar";
// import { presetStore } from "./Presets";


// new SharedToolbar();

const [combo, zoomIn, zoomOut, next, previous] = WidgetHelper.append([
   {
      type: 'combo',
      width: 200,
      ref: 'preset',
      placeholder: 'Preset',
      editable: false,
      hidden: true,
      // store: presetStore,
      displayField: 'name',
      value: 'hourAndDay',
      picker: {
         maxHeight: 500
      },
      onChange: () => {
         let schedule = window.bryntum.get('scheduler');
         schedule.zoomToLevel(combo.selected);
      }
   },
   {
      type: 'button',
      ref: 'zoomInButton',
      color: 'b-blue b-raised',
      icon: 'b-icon b-icon-search-plus',
      tooltip: 'Zoom in',
      onClick() {
         let schedule = window.bryntum.get('scheduler');
         schedule.zoomIn();
      }
   },
   {
      type: 'button',
      ref: 'zoomOutButton',
      color: 'b-blue b-raised',
      icon: 'b-icon b-icon-search-minus',
      tooltip: 'Zoom out',
      onClick() {
         let schedule = window.bryntum.get('scheduler');
         schedule.zoomOut();
      }
   },
   {
      type: 'button',
      icon: 'b-icon b-fa b-fa-angle-right',
      color: 'b-blue b-raised',
      tooltip: 'View next day',
      onAction() {
         let schedule = window.bryntum.get('scheduler');
         schedule.shiftNext();
      }
   },
   {
      type: 'button',
      icon: 'b-icon b-fa b-fa-angle-left',
      color: 'b-blue b-raised',
      tooltip: 'View previous day',
      onAction() {
         let schedule = window.bryntum.get('scheduler');
         schedule.shiftPrevious();
      }
   }

], { insertFirst: document.getElementById('tools') || document.body });