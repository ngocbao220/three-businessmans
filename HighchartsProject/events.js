// event.js
// Hàm xử lý sự kiện khi nhấp vào biểu tượng Pie Chart
// export function handlePieIconClick() {
//   document.getElementById("pie_icon").addEventListener("click", function () {
//     const pieChartContainer = document.getElementById("price_segment"); // Lấy phần tử DOM chứa biểu đồ pie
//     if (this.style.opacity === "0.5") {
//       this.style.opacity = "1";
//       pieChartContainer.style.opacity = "1"; // Hiển thị lại biểu đồ
//     } else {
//       this.style.opacity = "0.5";
//       pieChartContainer.style.opacity = "0"; // Làm mờ biểu đồ
//     }
//   });
// }

// // Hàm xử lý sự kiện khi nhấp vào biểu tượng Column Chart
// export function handleColumnIconClick() {
//   document.getElementById("column_icon").addEventListener("click", function () {
//     const columnChartContainer = document.getElementById("his_prices"); // Lấy phần tử DOM chứa biểu đồ column
//     if (this.style.opacity === "0.5") {
//       this.style.opacity = "1";
//       columnChartContainer.style.opacity = "1"; // Hiển thị lại biểu đồ
//     } else {
//       this.style.opacity = "0.5";
//       columnChartContainer.style.opacity = "0"; // Làm mờ biểu đồ
//     }
//   });
// }

// // Hàm xử lý sự kiện chuyển trang (Back)
// export function handleBackIconClick() {
//   document.getElementById("back_icon").addEventListener("click", function () {
//     const charts = document.querySelectorAll(".chart");
//     charts.forEach((chart) => {
//       chart.style.transform = "translateX(-1500px)";
//     });
//   });
// }

// // Hàm xử lý sự kiện chuyển trang (Next)
// export function handleNextIconClick() {
//   document.getElementById("next_icon").addEventListener("click", function () {
//     const charts = document.querySelectorAll(".chart");
//     charts.forEach((chart) => {
//       chart.style.transform = "translateX(0px)";
//     });
//   });
// }

// export function no_croll() {
//   document.addEventListener("DOMContentLoaded", () => {
//     document.body.addEventListener("click", (e) => {
//       const contextMenu = document.querySelector(".highcharts-contextmenu");

//       if (contextMenu && e.target.closest(".highcharts-contextmenu")) {
//         // Khi menu hiển thị
//         document.body.classList.add("no-scroll");
//       } else {
//         // Khi nhấp ra ngoài hoặc menu bị đóng
//         document.body.classList.remove("no-scroll");
//       }
//     });
//   });
// }
// const rect = c.getBoundingClientRect();

// // In ra tọa độ của phần tử c
// console.log("left:", rect.left);
// console.log("bottom:", rect.bottom);

let center_chart = null;

export function move(c, x, y) {
  const charts = document.querySelectorAll(".chart");

  // Reset styles for all charts
  charts.forEach((chart) => {
    chart.style.opacity = 0.7;
    chart.style.transform = "scale(0.8)";
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

  // Reset styles for all charts
  charts.forEach((chart) => {
    chart.style.opacity = 1;
    chart.style.transform = "translateX(0px) translateY(0px) scale(1)";
  });
}

export function typeText(elementId, text, delay = 100, hideDelay = 1000) {
  const element = document.getElementById(elementId);
  const bot_img = document.getElementById('bot')
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
  const charts = document.querySelectorAll('.chart');
  const subcharts = document.querySelectorAll('.subchart');

  charts.forEach((chart) => {
    chart.style.opacity = 0;
  })

  c.style.opacity = 1;
  c.style.transform = `translateX(${x}px) translateY(${y}px) scale(${scale})`;

  subcharts.forEach((subchart) => {
    subchart.style.opacity = 1;
  })
}