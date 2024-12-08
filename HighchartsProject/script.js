import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
  makeStdDevChart,
  makeVarianceChart,
} from "./chart.js";

import {set_Scene}
from "./events.js";

document.addEventListener("DOMContentLoaded", () => {
  // Gọi các hàm để tạo các biểu đồ
  makeSegmentPrice("area", "ha_noi", false, 0, 0, 96.3, 95, "segment");
  makeSegmentPrice("area", "ha_noi", false, 0, 0, 96.3, 95, "segment1");
  makeHistoryPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "history");
  makeCorrelation("area", "ha_noi", true, 0, 0, 96.3, 95, "correlation");
  makeNumPropertyType("area", "ha_noi", true, 0, 0, 96.3, 95, "type");
  makeStdDevChart("area", "ha_noi", false, 0, 0, 96.3, 95, "stddev");
  makeVarianceChart("area", "ha_noi", false, 0, 0, 96.3, 95, "variance");

  
  // Thiết lập cấu trúc
  set_Scene();

  
});
