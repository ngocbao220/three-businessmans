import {set_Scene, get_info_of_iframe, set_Event, update_list_chart, hideAllComment}
from "./eventForChart.js";

document.addEventListener("DOMContentLoaded", () => {
  update_list_chart('area','ha_noi');
  setTimeout(set_Event(), 2000);
  setTimeout(get_info_of_iframe(), 2000);
});
