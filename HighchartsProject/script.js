import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeSegmentCount,
  makeNumPropertyType,
  makeAveragePriceChart,
} from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {
  // Gọi các hàm từ chart.js
  makeSegmentPrice("area", "ha_noi", true);
  makeHistoryPrice("area", "ha_noi", true);
  makeCorrelation("area", "ha_noi", true);
  makeSegmentCount("area", "ha_noi", true);
  makeNumPropertyType("area", true); 
  makeAveragePriceChart("area", true);

  // Ví dụ khác
  // makeSegmentPrice("area", "nam_tu_liem", true, 0, 400, 30, 40);
});
