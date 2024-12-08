import {
  makeCorrelation,

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

function toggleDropdown() {
  const dropdownList = document.getElementById('dropdownList');
  if (dropdownList.style.display === 'block') {
      dropdownList.style.display = 'none';
  } else {
      dropdownList.style.display = 'block';
  }
}


const menu = document.getElementById("menu");
const asCenterBtn = document.getElementById("asCenter");
const returnBtn = document.getElementById("return");
const ShowMore = document.getElementById("showmore")
let currentCenter = document.getElementById("childCenter");
let lastSwapped = null;

// Function to open the menu
document.querySelectorAll(".action-btn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const rect = e.target.getBoundingClientRect();
    menu.style.top = `${rect.bottom}px`;
    menu.style.left = `${rect.left}px`;
    menu.style.display = "block";

    const parent = e.target.parentElement;
    asCenterBtn.style.display = parent === currentCenter ? "none" : "block";
    returnBtn.style.display = parent === currentCenter && lastSwapped ? "block" : "none";

    // Assign click events dynamically
    asCenterBtn.onclick = () => swapToCenter(parent);
    returnBtn.onclick = () => returnToLastSwapped();
    ShowMore.onclick = () => handleShowmoreClick(parent)

  });
});

  // Function to swap a div to the center
  function swapToCenter(selected) {
    if (selected === currentCenter) return;

    // Lấy tọa độ và kích thước hiện tại của các div
    const selectedRect = selected.getBoundingClientRect();
    const centerRect = currentCenter.getBoundingClientRect();

    // Tính toán khoảng cách di chuyển
    const deltaX = centerRect.left - selectedRect.left + 80;
    const deltaY = centerRect.top - selectedRect.top + 100;

    // Lưu kích thước ban đầu của các phần tử
    const selectedOriginalWidth = selected.style.width || `${selectedRect.width}px`;
    const selectedOriginalHeight = selected.style.height || `${selectedRect.height}px`;
    const centerOriginalWidth = currentCenter.style.width || `${centerRect.width}px`;
    const centerOriginalHeight = currentCenter.style.height || `${centerRect.height}px`;
  
    // Thay đổi kích thước và di chuyển thẻ cha
    selected.style.transition = "all 1s ease-in-out";
    currentCenter.style.transition = "all 1s ease-in-out";

    selected.style.width = centerOriginalWidth; // Đặt kích thước mới
    selected.style.height = centerOriginalHeight;
    selected.style.transform = `translate(${deltaX}px, ${deltaY}px)`;

    currentCenter.style.width = selectedOriginalWidth; // Đặt kích thước mới
    currentCenter.style.height = selectedOriginalHeight;
    currentCenter.style.transform = `translate(${-deltaX}px, ${-deltaY}px)`;

    menu.style.display = "none";

    setTimeout(() => {
        // Reset transform và hoán đổi các phần tử trong DOM
        selected.style.transform = "";
        currentCenter.style.transform = "";
        selected.style.width = "";
        selected.style.height = "";
        currentCenter.style.width = "";
        currentCenter.style.height = "";

        // Hoán đổi trong DOM
        const parentOfCenter = currentCenter.parentNode;
        const parentOfSelected = selected.parentNode;

        parentOfCenter.appendChild(selected);
        parentOfSelected.appendChild(currentCenter);

        // Cập nhật trạng thái
        lastSwapped = currentCenter;
        currentCenter = selected;
    }, 1000); // Thời gian đồng bộ với animation
}

// Function to return to the last swapped position
function returnToLastSwapped() {
  if (!lastSwapped) return;

  swapToCenter(lastSwapped);
}

// Close menu when clicking outside
// Function to handle showmore click
function handleShowmoreClick(parent) {
  // Get the showmore-board element
  const showmoreBoard = document.querySelector('.showmore-board');

  // Get bounding client rect of parent element
  const selectedRect = parent.getBoundingClientRect();
  const boardRect = showmoreBoard.getBoundingClientRect();

  // Calculate deltas
  const deltaX = boardRect.left + boardRect.width / 2 - (selectedRect.left + selectedRect.width / 2);
  const deltaY = boardRect.top + boardRect.height / 2 - (selectedRect.top + selectedRect.height / 2);

  // Calculate original sizes
  const selectedOriginalWidth = parent.style.width || `${selectedRect.width}px`;
  const selectedOriginalHeight = parent.style.height || `${selectedRect.height}px`;
  const scaleFactor = parent === currentCenter ? 0.8 : 1.4;
  // Loop through all child elements to fade and hide them
  document.querySelectorAll('.child').forEach((otherChild) => {
    if (otherChild !== parent) {
      otherChild.style.transition = 'opacity 0.8s ease';
      otherChild.style.opacity = 0;
      setTimeout(() => {
        otherChild.style.display = 'none';
      }, 800); // duration matches the fade out transition
    }
  });
  menu.style.display = "none";
  // Change size and move the selected element
  parent.style.transition = "all 1s ease-in-out";
  parent.style.width = selectedOriginalWidth;
  parent.style.height = selectedOriginalHeight;
  parent.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(${scaleFactor})`;

  parent.style.opacity = 1; parent.style.display = 'block';

  // After the transition, append the element to the showmore-board
  setTimeout(() => {
    if(scaleFactor == 0.8){
      parent.style.transform = "scale(0.8)"; 
    }
    else parent.style.transform = "scale(1.4)"; 
    parent.style.width = ""; 
    parent.style.height = ""; // Append the parent element to showmore-board 
    showmoreBoard.appendChild(parent);
    showmoreBoard.style.pointerEvents = "auto";
  }, 1000);
}


export function show_amount(month1, month2, difference) {
  const fta_para = document.getElementById("fta-para");
  const text_container = document.getElementById("fta_comment");
  const icon_up = document.getElementById("icon_up");
  const icon_down = document.getElementById("icon_down");
  const fta_num = document.getElementById("fta-number");

  // Kiểm tra biến động giá
  if (difference < 0) {
    icon_up.style.display = "none"; // Ẩn biểu tượng tăng
    icon_down.style.display = "block"; // Hiện biểu tượng giảm
    text_container.style.borderColor = "red"; // Đổi màu viền sang đỏ
    const text = `Giá tại khu vực giảm, từ ${month1} đến ${month2}`;
    fta_para.innerHTML = `<strong>${text}</strong>`; // Cập nhật nội dung và in đậm
  } else {
    icon_down.style.display = "none"; // Ẩn biểu tượng giảm
    icon_up.style.display = "block"; // Hiện biểu tượng tăng
    text_container.style.borderColor = "green"; // Đổi màu viền sang xanh
    const text = `Giá tại khu vực tăng, từ ${month1} đến ${month2}`;
    fta_para.innerHTML = `<strong>${text}</strong>`;
  }

  // Hiển thị tỷ lệ biến động giá
  fta_num.innerHTML = `<strong>${
    Math.round(Math.abs(difference) * 10) / 10
  } %</strong>`; // Dùng giá trị tuyệt đối và in đậm
}
