import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
} from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {
  makeSegmentPrice("area", "ha_noi", true);
  makeHistoryPrice("area", "ha_noi", true);
  makeCorrelation("area", "ha_noi", true);

  // makeSegmentPrice("area", "nam_tu_liem", true, 0, 400, 30, 40);
});
