import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
} from "./chart.js";

import {set_Scene}
from "./events.js";

document.addEventListener("DOMContentLoaded", () => {
  // Gọi các hàm để tạo các biểu đồ
  makeSegmentPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "segment");
  makeHistoryPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "history");
  makeCorrelation("area", "ha_noi", true, 0, 0, 96.3, 95, "correlation");
  makeNumPropertyType("area", "ha_noi", true, 0, 0, 96.3, 95, "type");
  set_Scene();
});
