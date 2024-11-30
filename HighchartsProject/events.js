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
    }, 1000);
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
  if (c == segment) {
    makeSegmentPrice('area', 'bac_tu_liem', false, 400, 200, 30, 40, 'sub_chart_of_pie');
  }
}


export function remake_sub_chart_of_Pie(range_name) {
  const sub_charts = document.querySelectorAll(".sub_chart_of_pie");
  let jsonFilePath;

  // Xác định đường dẫn tệp JSON theo range_name
  switch (range_name) {
    case "Dưới 50 triệu/m²":
      jsonFilePath = "../Data/Json/Segment/area/ha_dong.json";
      break;
    // case "50 đến 100 triệu/m²":
    //   jsonFilePath = "../Data/Json/Segment/segment/type2.json";
    //   break;
    // case "100 đến 150 triệu/m²":
    //   jsonFilePath = "../Data/Json/Segment/segment/type3.json";
    //   break;
    // case "150 đến 200 triệu/m²":
    //   jsonFilePath = "../Data/Json/Segment/segment/type4.json";
    //   break;
    // case "Trên 200 triệu/m²":
    //   jsonFilePath = "../Data/Json/Segment/segment/type5.json";
    //   break;
    default:
      console.error("Giá trị range_name không hợp lệ:", range_name);
      return; // Kết thúc hàm nếu không xác định được JSON
  }

  // Duyệt qua các biểu đồ
  sub_charts.forEach((sub_chart) => {
    console.log(sub_chart.id);

    if (sub_chart) {
      // Tải dữ liệu JSON và cập nhật biểu đồ
      fetch(jsonFilePath)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((newData) => {
          if (sub_chart && sub_chart.series[0] && Array.isArray(newData)) {
            sub_chart.series[0].setData(newData);
            console.log(
              `Dữ liệu biểu đồ #${sub_chart.highchartsChart} đã được cập nhật!`
            );
          } else {
            console.error("Dữ liệu JSON không hợp lệ:", newData);
          }
        })
        .catch((error) => {
          console.error("Lỗi khi tải hoặc cập nhật dữ liệu:", error);
        });
    } else {
      console.error(
        "Không tìm thấy biểu đồ hoặc biểu đồ không hợp lệ:",
        sub_chart
      );
    }
  });
}
