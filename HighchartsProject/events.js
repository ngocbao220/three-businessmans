import {
  makeSegmentPrice,
  makeCorrelation,
  makeHistoryPrice,
  makeNumPropertyType,
} from "./chart.js";

function normalizeName(areaName) {
  // Bỏ dấu tiếng Việt
  areaName = areaName.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  // Thay thế các ký tự đặc biệt
  areaName = areaName.replace(/đ/g, "d");
  areaName = areaName.replace(/Đ/g, "d");
  areaName = areaName.replace(/_/g, " ");
  areaName = areaName.replace(/-/g, " ");

  // Chuyển tất cả sang chữ thường
  areaName = areaName.toLowerCase();

  // Thay khoảng trắng và các ký tự không hợp lệ bằng dấu gạch dưới
  areaName = areaName.replace(/\s+|, /g, "_");

  return areaName;
}

export function move(c, x, y) {
  const charts = document.querySelectorAll(".chart");

  // Reset styles for all charts
  charts.forEach((chart) => {
    chart.style.opacity = 0.7;
    chart.style.transform = "scale(0.8)";
    chart.style.pointerEvents = "auto";
  });

  // Highlight the target chart
  c.style.opacity = 1;
  c.style.transform = `translateX(${x}px) translateY(${y}px) scale(1.2)`;

  // Reset previous center chart if it's not the current chart
  if (center_chart && center_chart !== c) {
    center_chart.style.transform = "translateX(0px) translateY(0px) scale(0.8)";
  }

  // Update the center chart
  center_chart = c;
}

export function returnToDefalut() {
  const charts = document.querySelectorAll(".chart");
  const sub_chart = document.querySelectorAll(".sub_chart");
  // Reset styles for all charts
  charts.forEach((chart) => {
    chart.style.opacity = 1;
    chart.style.transform = "translateX(0px) translateY(0px) scale(1)";
    chart.style.pointerEvents = "auto";
  });

  sub_chart.forEach((chart) => {
    chart.style.opacity = 0;
    setTimeout(() => {
      chart.remove();
    }, 2000);
  });
}

export function show_amount(month1, month2, difference) {
  const fta_para = document.getElementById("fta-para");
  const text_container = document.getElementById("fluctuation");
  const icon_up = document.getElementById("icon_up");
  const icon_down = document.getElementById("icon_down");
  const fta_num = document.getElementById("fta-number");

  // Kiểm tra biến động giá
  if (difference < 0) {
    icon_up.style.display = "none"; // Ẩn biểu tượng tăng
    icon_down.style.display = "block"; // Hiện biểu tượng giảm
    text_container.style.borderColor = "red"; // Đổi màu viền sang đỏ
    const text = `Từ ${month1} đến ${month2}, giá trung bình giảm`;
    fta_para.innerHTML = `<strong>${text}</strong>`; // Cập nhật nội dung và in đậm
  } else {
    icon_down.style.display = "none"; // Ẩn biểu tượng giảm
    icon_up.style.display = "block"; // Hiện biểu tượng tăng
    text_container.style.borderColor = "green"; // Đổi màu viền sang xanh
    const text = `Từ ${month1} đến ${month2}, giá trung bình tăng`;
    fta_para.innerHTML = `<strong>${text}</strong>`;
  }

  // Hiển thị tỷ lệ biến động giá
  fta_num.innerHTML = `<strong>${
    Math.round(Math.abs(difference) * 10) / 10
  } %</strong>`; // Dùng giá trị tuyệt đối và in đậm
}

export function showmore(c, x, y, scale = 1) {
  const charts = document.querySelectorAll(".chart");

  charts.forEach((chart) => {
    chart.style.opacity = 0;
    chart.style.pointerEvents = "none";
  });

  c.style.opacity = 1;
  c.style.pointerEvents = "auto";
  c.style.transform = `translateX(${x}px) translateY(${y}px) scale(${scale})`;

  const segment = document.getElementById("price_segment_of_ha_noi");
  const history_price = document.getElementById("history_price_of_ha_noi");
  const number_of_type_property = document.getElementById(
    "column_chart_of_count_classify_of_ha_noi"
  );
  if (c == segment) {
    makeCorrelation("segment", "under_50", false, 900, 0, 30, 50, "sub_chart");
    makeNumPropertyType("segment");
  } else if (c == number_of_type_property) {
    makeHistoryPrice(
      "type",
      "can_ho_chung_cu",
      false,
      600,
      200,
      30,
      40,
      "sub_chart"
    );
  }
}

export function remake_sub_chart_of_Pie(range_name) {
  const sub_charts = document.querySelectorAll(".sub_chart");
  let name;
  // Xác định đường dẫn tệp JSON theo range_name
  switch (range_name) {
    case "Dưới 50 triệu/m²":
      name = "under_50";
      break;
    case "50 đến 100 triệu/m²":
      name = "between_50_100";
      break;
    case "100 đến 150 triệu/m²":
      name = "between_100_150";
      break;
    case "150 đến 200 triệu/m²":
      name = "between_150_200";
      break;
    case "Trên 200 triệu/m²":
      name = "over_200";
      break;
    default:
      console.error("Giá trị range_name không hợp lệ:", range_name);
      return;
  }

  sub_charts.forEach((sub_chart) => {
    sub_chart.remove();
  });

  makeCorrelation("segment", name, false, 900, 0, 30, 50, "sub_chart");
}

export function remake_sub_chart_of_Column(range_name) {
  const sub_charts = document.querySelectorAll(".sub_chart");
  let name = normalizeName(range_name);

  sub_charts.forEach((sub_chart) => {
    sub_chart.remove();
  });

  makeHistoryPrice("type", name, false, 900, 0, 30, 50, "sub_chart");
}

export function remove_sub_chart() {
  const sub_charts = document.querySelectorAll(".sub_chart");

  sub_charts.forEach((chart) => {
    chart.style.opacity = 0;
    setTimeout(() => {
      chart.remove();
    }, 2000);
  });
}


export function set_Scene() {
  // Đợi biểu đồ được tạo
  setTimeout(() => {
    console.log("Biểu đồ đã được khởi tạo");

    // Danh sách phần tử cần lướt
    const charts = [
      document.getElementById("segment"),
      document.getElementById("history"),
      document.getElementById("type"),
      document.getElementById("correlation"),
    ];

    // Nút điều hướng
    let fta = document.getElementById("fluctuation");
    const btnRight = document.getElementById("btnRight");
    const btnLeft = document.getElementById("btnLeft");

    // Khởi tạo trạng thái
    let currentIndex = 0;
    const totalCharts = charts.length;

    // Thiết lập CSS ban đầu cho các biểu đồ
    charts.forEach((chart, index) => {
      chart.style.transform = `translateX(${index * 100}%)`;
      chart.style.transition = "transform 0.5s";
    });

    // Xử lý sự kiện nút Right
    btnRight.addEventListener("click", () => {
      if (currentIndex < totalCharts - 1) {
        currentIndex++;
        if (currentIndex == 1) {
          fta.style.display = 'block';
        } else fta.style.display = 'none';
        updateChartPosition();
        updateButtonState();
      }
    });

    // Xử lý sự kiện nút Left
    btnLeft.addEventListener("click", () => {
      if (currentIndex > 0) {
        currentIndex--;
        if (currentIndex == 1) {
          fta.style.display = 'block';
        } else fta.style.display = 'none';
        updateChartPosition();
        updateButtonState();
      }
    });

    // Hàm cập nhật vị trí biểu đồ
    function updateChartPosition() {
      charts.forEach((chart, index) => {
        chart.style.transform = `translateX(${(index - currentIndex) * 100}%)`;
      });
    }

    // Hàm cập nhật trạng thái nút
    function updateButtonState() {
      btnLeft.style.opacity = currentIndex === 0 ? 0.3 : 1;
      btnLeft.style.cursor = currentIndex === 0 ? "default" : "pointer";
      btnRight.style.opacity = currentIndex === totalCharts - 1 ? 0.3 : 1;
      btnRight.style.cursor = currentIndex === totalCharts - 1 ? "default" : "pointer";
    }

    // Cập nhật trạng thái nút ban đầu
    updateButtonState();
  }, 1000);
}