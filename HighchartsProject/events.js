let center_chart = null;
import {
  makeSegmentPrice,
  makeCorrelation,
  makeHistoryPrice,
} from "./chart.js";

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
  const sub_chart = document.querySelectorAll(".sub_chart_of_pie");
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
  })
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
  if (c == segment) {
    makeCorrelation('segment', 'under_50', false, 700, 400, 30, 40, 'sub_chart_of_pie');
    makeHistoryPrice('segment', 'under_50', false, 800, 0, 40, 50, 'sub_chart_of_pie');
  } else if (c == history_price) {
    
  }
}


export function remake_sub_chart_of_Pie(range_name) {
  const sub_charts = document.querySelectorAll(".sub_chart_of_pie");
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
      name =  "between_100_150";
      break;
    case "150 đến 200 triệu/m²":
      name = "between_150_200";
      break;
    case "Trên 200 triệu/m²":
      name = "over_200";
      break;
    default:
      console.error("Giá trị range_name không hợp lệ:", range_name);
      return; // Kết thúc hàm nếu không xác định được JSON
  }

  // Duyệt qua các biểu đồ
  sub_charts.forEach((sub_chart) => {
    sub_chart.remove();
  })

  makeCorrelation('segment', name, false, 700, 400, 30, 40, 'sub_chart_of_pie');
  makeHistoryPrice('segment', name, false, 700, 100, 30, 40, 'sub_chart_of_pie');
}
