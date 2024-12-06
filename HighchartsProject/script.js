import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
} from "./chart.js";

document.addEventListener("DOMContentLoaded", () => {
  // Gọi các hàm để tạo các biểu đồ
  makeSegmentPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "segment");
  makeHistoryPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "history");

  // Sử dụng setTimeout để đợi biểu đồ cập nhật
  setTimeout(() => {
    console.log("Đã đợi 1 giây");

    // Thực hiện hành động sau khi đợi
    let segment = document.getElementById("segment");
    let history = document.getElementById("history");

    history.style.transform = 'translateX(550px)';
    history.style.transition = "transform 0.5s";
    segment.style.transition = "transform 0.5s";

    document.getElementById("btnRight").addEventListener("click", function () {
      segment.style.transform = "translateX(-550px)"; // Di chuyển segment sang trái
      history.style.transform = "translateX(0px)"; // Di chuyển history sang trái
    });

    document.getElementById("btnLeft").addEventListener("click", function () {
      segment.style.transform = "translateX(0px)"; // Di chuyển segment sang trái
      history.style.transform = "translateX(550px)"; // Di chuyển history sang trái
    });
  }, 1000);
});
