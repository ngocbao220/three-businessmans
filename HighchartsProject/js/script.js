import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
} from "./createCharts.js";

import {set_Scene, get_info_of_iframe, set_Event}
from "./eventForChart.js";

document.addEventListener("DOMContentLoaded", () => {
  // Gọi các hàm để tạo các biểu đồ
  makeSegmentPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "segment");
  makeHistoryPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "history");
  makeCorrelation("area", "ha_noi", true, 0, 0, 96.3, 95, "correlation");
  makeNumPropertyType("area", "ha_noi", true, 0, 0, 96.3, 95, "type");

  // Thiết lập cấu trúc
  // set_Scene();
  // set_Event();
  // get_info_of_iframe();

  setTimeout(set_Scene(), 1000);
  setTimeout(set_Event(), 1000);
  setTimeout(get_info_of_iframe(), 1000);
});
