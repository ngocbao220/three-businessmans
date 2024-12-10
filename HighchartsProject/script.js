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

import { set_Scene } from "./events.js";

document.addEventListener("DOMContentLoaded", () => {
  // Gọi các hàm để tạo các biểu đồ
  
  // Hàm vẽ biểu đồ cho StdDev và Variance
  function drawStdAndVarChart(district) {
    // Thực hiện gọi các hàm vẽ biểu đồ với tham số quận huyện
    makeSegmentPrice("area", district, false, 0, 0, 96.3, 95, "segment1");
  }

  // Lắng nghe sự kiện thay đổi giá trị quận huyện
  const districtSelect = document.getElementById("district");
  
  if (districtSelect) {
    districtSelect.addEventListener("change", (event) => {
      const selectedDistrict = event.target.value;
      drawStdAndVarChart(selectedDistrict); // Gọi hàm vẽ biểu đồ khi người dùng chọn quận huyện
    });
  } else {
    console.error('Không tìm thấy phần tử với ID "district"');
  }

  // Thiết lập cấu trúc
  set_Scene();
});
