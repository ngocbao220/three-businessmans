// event.js
// Hàm xử lý sự kiện khi nhấp vào biểu tượng Pie Chart
export function handlePieIconClick() {
  document.getElementById("pie_icon").addEventListener("click", function () {
    const pieChartContainer = document.getElementById("price_segment"); // Lấy phần tử DOM chứa biểu đồ pie
    if (this.style.opacity === "0.5") {
      this.style.opacity = "1";
      pieChartContainer.style.opacity = "1"; // Hiển thị lại biểu đồ
    } else {
      this.style.opacity = "0.5";
      pieChartContainer.style.opacity = "0"; // Làm mờ biểu đồ
    }
  });
}

// Hàm xử lý sự kiện khi nhấp vào biểu tượng Column Chart
export function handleColumnIconClick() {
  document.getElementById("column_icon").addEventListener("click", function () {
    const columnChartContainer = document.getElementById("his_prices"); // Lấy phần tử DOM chứa biểu đồ column
    if (this.style.opacity === "0.5") {
      this.style.opacity = "1";
      columnChartContainer.style.opacity = "1"; // Hiển thị lại biểu đồ
    } else {
      this.style.opacity = "0.5";
      columnChartContainer.style.opacity = "0"; // Làm mờ biểu đồ
    }
  });
}

// Hàm xử lý sự kiện chuyển trang (Back)
export function handleBackIconClick() {
  document.getElementById("back_icon").addEventListener("click", function () {
    const charts = document.querySelectorAll(".chart");
    charts.forEach((chart) => {
      chart.style.transform = "translateX(-1500px)";
    });
  });
}

// Hàm xử lý sự kiện chuyển trang (Next)
export function handleNextIconClick() {
  document.getElementById("next_icon").addEventListener("click", function () {
    const charts = document.querySelectorAll(".chart");
    charts.forEach((chart) => {
      chart.style.transform = "translateX(0px)";
    });
  });
}

let isCentered = false; // Biến kiểm tra trạng thái (ban đầu chưa căn giữa)

export function toggleCenter(c) {
  const charts = document.querySelectorAll(".chart"); // Lấy tất cả các phần tử có class 'chart'

  if (!isCentered) {
    charts.forEach((chart) => {
      chart.style.opacity = "0"; // Làm mờ tất cả các biểu đồ
    });

    // Làm sáng biểu đồ trung tâm
    c.style.opacity = "1"; // Làm sáng biểu đồ c
    c.style.transform = "translateX(-700px) translateY(-150px) scale(1.2)"; // Căn giữa biểu đồ ở vị trí chính giữa bên trái

    isCentered = true; // Đánh dấu là đã căn giữa

    // Thay đổi tên menu item thành "Not be center"
    const contextButton = document.querySelector(".highcharts-contextbutton");
    const menuItems = contextButton.querySelectorAll("li");
    const firstMenuItem = menuItems[0];
    firstMenuItem.textContent = "Notbecenter";
  } else {
    charts.forEach((chart) => {
      chart.style.opacity = "1"; // Làm sáng tất cả các biểu đồ
      chart.style.transform = "scale(1)"; // Đặt lại kích thước của các biểu đồ
    });

    c.style.transform = "translateX(0) translateY(0)"; // Đưa về vị trí ban đầu

    isCentered = false; // Đánh dấu là chưa căn giữa

    // Thay đổi tên menu item thành "beCenter"
    const contextButton = document.querySelector(".highcharts-contextbutton");
    const menuItems = contextButton.querySelectorAll("li");
    const firstMenuItem = menuItems[0];
    firstMenuItem.textContent = "beCenter";
  }
}



