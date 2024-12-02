function toggleDropdown() {
    const dropdownList = document.getElementById('dropdownList');
    if (dropdownList.style.display === 'block') {
        dropdownList.style.display = 'none';
    } else {
        dropdownList.style.display = 'block';
    }
}

// Close the dropdown if clicked outside
window.onclick = function(event) {
    const dropdownList = document.getElementById('dropdownList');
    const button = document.querySelector('.dropdown-button');
    if (!button.contains(event.target) && !dropdownList.contains(event.target)) {
        dropdownList.style.display = 'none';
    }
};
function swapWithAnimation() {
    const child1 = document.getElementById('child1');
    const child2 = document.getElementById('child2');
  
    // Lấy tọa độ hiện tại của hai phần tử
    const rect1 = child1.getBoundingClientRect();
    const rect2 = child2.getBoundingClientRect();
  
    // Tính khoảng cách di chuyển
    const deltaX1 = rect2.left - rect1.left;
    const deltaY1 = rect2.top - rect1.top;
  
    const deltaX2 = rect1.left - rect2.left;
    const deltaY2 = rect1.top - rect2.top;
  
    // Thêm class để tạo hiệu ứng
    child1.classList.add('moving');
    child2.classList.add('moving');
  
    // Di chuyển các phần tử
    child1.style.transform = `translate(${deltaX1}px, ${deltaY1}px)`;
    child2.style.transform = `translate(${deltaX2}px, ${deltaY2}px)`;
  
    // Sau khi animation kết thúc, đổi chỗ thật sự
    setTimeout(() => {
      child1.classList.remove('moving');
      child2.classList.remove('moving');
  
      // Reset vị trí
      child1.style.transform = '';
      child2.style.transform = '';
  
      // Thực sự đổi chỗ
      const parent1 = child1.parentNode;
      const parent2 = child2.parentNode;
  
      parent1.appendChild(child2);
      parent2.appendChild(child1);
    }, 1000); // Thời gian khớp với duration của animation (1s)
  }
  const menu = document.getElementById("menu");
  const asCenterBtn = document.getElementById("asCenter");
  const returnBtn = document.getElementById("return");
  
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
    });
  });
  
  // Function to swap a div to the center
  function swapToCenter(selected) {
    if (selected === currentCenter) return;

    // Lấy tọa độ và kích thước hiện tại của các div
    const selectedRect = selected.getBoundingClientRect();
    const centerRect = currentCenter.getBoundingClientRect();

    // Tính toán khoảng cách di chuyển
    const deltaX = centerRect.left - selectedRect.left + 20;
    const deltaY = centerRect.top - selectedRect.top + 75;

    // Lưu kích thước ban đầu của các phần tử
    const selectedOriginalWidth = selected.style.width || `${selectedRect.width}px`;
    const selectedOriginalHeight = selected.style.height || `${selectedRect.height}px`;
    const centerOriginalWidth = currentCenter.style.width || `${centerRect.width}px`;
    const centerOriginalHeight = currentCenter.style.height || `${centerRect.height}px`;

    // Thay đổi kích thước và di chuyển
    const selectedChildren = selected.querySelectorAll(".childrent");
    const centerChildren = currentCenter.querySelectorAll(".childrent");
    selected.style.transition = "all 1s ease-in-out";
    currentCenter.style.transition = "all 1s ease-in-out";

    selected.style.width = centerOriginalWidth; // Đặt kích thước mới
    selected.style.height = centerOriginalHeight;
    selected.style.transform = `translate(${deltaX}px, ${deltaY}px)`;

    currentCenter.style.width = selectedOriginalWidth; // Đặt kích thước mới
    currentCenter.style.height = selectedOriginalHeight;
    currentCenter.style.transform = `translate(${-deltaX}px, ${-deltaY}px)`;

    selectedChildren.forEach(child => {
      child.style.transition = "all 1s ease-in-out";
      child.style.transform = "translate(0, 0)"; // Giữ ở trung tâm
  });

  centerChildren.forEach(child => {
      child.style.transition = "all 1s ease-in-out";
      child.style.transform = "translate(0, 0)"; // Giữ ở trung tâm
  });
    menu.style.display = "none";

    setTimeout(() => {
        // Reset transform và hoán đổi các phần tử trong DOM
        selected.style.transform = "";
        currentCenter.style.transform = "";

        // Đặt lại kích thước về trạng thái mặc định để chuẩn bị cho lần hoán đổi tiếp theo
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


// Hàm để quay lại vị trí đã hoán đổi cuối cùng
function returnToLastSwapped() {
    if (!lastSwapped) return;

    swapToCenter(lastSwapped);
}
  
  // Close menu when clicking outside
  document.addEventListener("click", (e) => {
    if (!menu.contains(e.target) && !e.target.classList.contains("action-btn")) {
      menu.style.display = "none";
    }
  });
  
  