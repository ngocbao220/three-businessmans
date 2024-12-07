import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
} from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {
  makeSegmentPrice("area", "ha_noi", true, 930, 400, 30, 40, 'chart');
  makeHistoryPrice("area", "ha_noi", true, 930, 0, 30, 50, 'chart');
  makeNumPropertyType('area', 'ha_noi', true, 0, 380, 30, 40, 'chart');
  makeAveragePriceChart('area', 'ha_noi', true, 930, 400, 30, 40, 'chart' );
});
