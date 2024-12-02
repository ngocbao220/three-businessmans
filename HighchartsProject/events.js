import {
  makeSegmentPrice,
  makeCorrelation,
  makeHistoryPrice,
  makeNumPropertyType,
} from "./chart.js";

function normalizeName(areaName) {
  // Bỏ dấu tiếng Việt
  areaName = areaName.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  
  // Thay thế các ký tự đặc biệt
  areaName = areaName.replace(/đ/g, 'd');
  areaName = areaName.replace(/Đ/g, 'd');
  areaName = areaName.replace(/_/g, ' ');
  areaName = areaName.replace(/-/g, ' ');

  // Chuyển tất cả sang chữ thường
  areaName = areaName.toLowerCase();

  // Thay khoảng trắng và các ký tự không hợp lệ bằng dấu gạch dưới
  areaName = areaName.replace(/\s+|, /g, '_');

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

export function typeText(elementId, text, delay = 100, hideDelay = 1000) {
  const element = document.getElementById(elementId);
  const bot_img = document.getElementById("bot");
  bot_img.style.opacity = 1;
  element.style.opacity = 1;
  element.textContent = "";
  let index = 0;

  // Hàm hiển thị từng ký tự
  function type() {
    if (index < text.length) {
      element.textContent += text.charAt(index); // Thêm từng ký tự
      index++;
      setTimeout(type, delay); // Tiếp tục gọi lại chính nó với delay
    } else {
      // Khi gõ xong, bắt đầu hiệu ứng ẩn sau hideDelay
      setTimeout(() => {
        element.style.transition = "opacity 0.5s ease"; // Hiệu ứng mờ dần
        element.style.opacity = 0;
        bot_img.style.opacity = 0;
      }, hideDelay);
    }
  }

  type(); // Bắt đầu hiệu ứng
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
  const number_of_type_property = document.getElementById('column_chart_of_count_classify_of_ha_noi')
  if (c == segment) {
    makeCorrelation(
      "segment",
      "under_50",
      false,
      900,
      0,
      30,
      50,
      "sub_chart"
    );
    makeNumPropertyType('segment', )
  } else if (c == number_of_type_property) {
    makeHistoryPrice('type', 'can_ho_chung_cu', false, 600, 200, 30, 40, 'sub_chart');
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
