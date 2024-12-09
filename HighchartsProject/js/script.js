import {
  makeSegmentPrice,
  makeHistoryPrice,
  makeCorrelation,
  makeAveragePriceChart,
  makeNumPropertyType,
  makeSegmentCount,
} from "./createCharts.js";

import {set_Scene, get_info_of_iframe, set_Event, update_list_chart}
from "./eventForChart.js";

document.addEventListener("DOMContentLoaded", () => {
<<<<<<< HEAD
  // Gọi các hàm để tạo các biểu đồ
  makeSegmentPrice("area", "ha_noi", false, 0, 0, 96.3, 95, "segment");
  makeSegmentPrice("area", "ha_noi", false, 0, 0, 96.3, 95, "segment1");
  makeHistoryPrice("area", "ha_noi", true, 0, 0, 96.3, 95, "history");
  makeCorrelation("area", "ha_noi", true, 0, 0, 96.3, 95, "correlation");
  makeNumPropertyType("area", "ha_noi", true, 0, 0, 96.3, 95, "type");

  // Hàm vẽ biểu đồ cho StdDev và Variance
  function drawStdAndVarChart(district) {
    // Thực hiện gọi các hàm vẽ biểu đồ với tham số quận huyện
    makeStdDevChart("area", district, false, 0, 0, 96.3, 95, "stddev");
    makeVarianceChart("area", district, false, 0, 0, 96.3, 95, "variance");
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
  // set_Scene();
  // set_Event();
  // get_info_of_iframe();

  setTimeout(set_Scene(), 1000);
=======
  update_list_chart('area','ha_noi');
>>>>>>> ngocbao
  setTimeout(set_Event(), 1000);
  setTimeout(get_info_of_iframe(), 1000);
});
