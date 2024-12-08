import {
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
} from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {

  makeNumPropertyType('area', 'ha_noi', true,930, 400, 30, 40, 'chart');
  makeAveragePriceChart('area', 'ha_noi', true, 930, 400, 30, 40, 'chart' );
});
