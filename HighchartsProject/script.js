import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
} from "./makechart.js";

document.addEventListener("DOMContentLoaded", () => {
  makeSegmentPrice("area", "ha_noi", true);
  makeHistoryPrice("area", "ha_noi", true);
  makeCorrelation("area", "ha_noi", true);

});