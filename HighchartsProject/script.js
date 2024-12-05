import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
} from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {
  // makeSegmentPrice("area", "ha_noi", true, 930, 400, 30, 40, 'chart');
  makeHistoryPrice("area", "ha_noi", true, 700, 30, 40, 50, 'chart');
});

