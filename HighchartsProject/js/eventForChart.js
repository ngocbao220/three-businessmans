import {
  makeSegmentPrice,
  makeCorrelation,
  makeHistoryPrice,
  makeNumPropertyType,
} from "./createCharts.js";

// Nút điều hướng
const btnRight = document.getElementById("btnRight");
const btnLeft = document.getElementById("btnLeft");

// Bản đồ nhiệt
const district_map = document.querySelector(".district_map");
const district = document.querySelector(".district");

const ward_map = document.querySelector(".ward_map");
const ward = document.querySelector(".ward");

// Nút chuyển trạng thái xem
const btn_project = document.getElementById("btn-project");
const lst_project = document.getElementById("lst-project");

// Mắt xem chi tiết quận/huyện
const eye = document.getElementById("eye");

// Thẻ thông tin dự án
const pro_info = document.querySelector(".card-info");

// Thẻ title
const map_title = document.getElementById("heat_title");
const pro_title = document.getElementById("lst-pro-title");

// Comment
const comments = [
  document.getElementById("sgm_comment"),
  document.getElementById("fta_comment"),
  document.getElementById("type_comment"),
  document.getElementById("crl_comment"),
];

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

let isDeeplyVisible = false;

function see_deeply() {
  if (!isDeeplyVisible) {
    // Thu nhỏ bản đồ quận/huyện
    ward_map.style.display = "block";
    district_map.style.width = "15%";
    district_map.style.height = "30%";

    district_map.style.transform = "translateX(-293px) translateY(-368px)";

    // Thay đổi nút
    document.getElementById("eye").style.opacity = 0.5;

    hideAllComment();
  } else {
    ward_map.style.display = "none";
    district_map.style.width = "40%";
    district_map.style.height = "80%";

    district_map.style.transform = "translateX(-49%) translateY(-355px)";

    // Thay đổi nút
    document.getElementById("eye").style.opacity = 1;

    update_list_chart("area", "ha_noi");
    set_Scene();

    map_title.style.display = "block";
    map_title.innerHTML = "Khu vực hiện tại: Hà Nội";
    showAllComment();
  }

  // Cập nhật trạng thái
  isDeeplyVisible = !isDeeplyVisible;
}

export function update_list_chart(type, district) {
  setTimeout(
    makeSegmentPrice(type, district, true, 0, 0, 96.3, 95, "segment"),
    1000
  );
  setTimeout(
    makeHistoryPrice(type, district, true, 0, 0, 96.3, 95, "history"),
    1000
  );
  setTimeout(
    makeCorrelation(type, district, true, 0, 0, 96.3, 95, "correlation"),
    1000
  );
  setTimeout(
    makeNumPropertyType(type, district, true, 0, 0, 96.3, 95, "type"),
    1000
  );

  setTimeout(set_Scene(), 1000);
}

district.addEventListener("load", () => {
  // Truy cập vào nội dung bên trong iframe
  const iframeWindow = district.contentWindow;
  const iframeDocument = iframeWindow.document;

  // Tìm tất cả các lớp GeoJSON trên bản đồ
  const geoJsonLayers = Object.values(iframeWindow).filter(
    (layer) => layer instanceof iframeWindow.L.GeoJSON
  );

  if (geoJsonLayers.length === 0) {
    console.error("Không tìm thấy lớp GeoJSON trên bản đồ!");
    return;
  }

  geoJsonLayers.forEach((layer) => {
    layer.eachLayer((featureLayer) => {
      featureLayer.on("click", () => {
        // Lấy tên khu vực từ thuộc tính GeoJSON
        const districtName = featureLayer.feature.properties.NAME_2;
        if (!districtName) return;

        const formattedName = normalizeName(districtName);
        const newSrc = `../html/data_for_map/${formattedName}.html`;

        // Cập nhật src cho iframe xã/phường
        ward.src = newSrc;
        // Thay đổi biểu đồ liên quan
        if (isDeeplyVisible) {
          update_list_chart("area", formattedName);
          map_title.innerHTML = `Khu vực hiện tại: ${districtName}`;
        }

        console.log(`Chuyển sang bản đồ xã/phường: ${newSrc}`);
      });
    });
  });
});

export function get_info_of_iframe(
  iframe_id = "lst-project",
  ele_class = ".project-card"
) {
  const iframe = document.getElementById(iframe_id);

  iframe.onload = function () {
    // Kiểm tra xem iframe đã tải đầy đủ chưa
    if (!iframe.contentDocument) {
      console.error("Không thể truy cập nội dung iframe");
      return;
    } else {
      console.log("Đã kích hoạt được iframe");
    }

    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    const elements = iframeDoc.querySelectorAll(ele_class);
    let previousElement = null;

    elements.forEach((element) => {
      element.addEventListener("click", () => {
        if (previousElement) {
          previousElement.style.backgroundColor = "";
        }

        element.style.backgroundColor = "#F5F0CD";

        // Cập nhật phần tử được click trước đó
        previousElement = element;

        const details = element.querySelector(".details");

        // Tên dự án
        const projectNameElement = element.querySelector("h2");
        const projectName =
          projectNameElement?.textContent.trim() || "Tên dự án không có sẵn";

        // Lượt xem
        const views =
          element.querySelectorAll("p")[0]?.textContent.trim() ||
          "Không có lượt xem";

        // Chủ đầu tư
        const investor =
          element.querySelectorAll("p")[1]?.textContent.trim() ||
          "Không có thông tin chủ đầu tư";

        // Quận/Huyện
        const district =
          element.querySelectorAll("p")[2]?.textContent.trim() ||
          "Không có thông tin quận/huyện";

        // Pháp lý
        const legalStatus =
          element.querySelectorAll("p")[3]?.textContent.trim() ||
          "Không có thông tin pháp lý";

        // Thông tin chi tiết (Diện tích, Số căn hộ, Số tòa, Tiện ích)
        const area =
          details.querySelector("p:nth-child(1)")?.textContent.trim() ||
          "Không có thông tin diện tích";
        const apartments =
          details.querySelector("p:nth-child(2)")?.textContent.trim() ||
          "Không có thông tin số căn hộ";
        const buildings =
          details.querySelector("p:nth-child(3)")?.textContent.trim() ||
          "Không có thông tin số tòa";
        
        const minPrice =
        details.querySelector("p:nth-child(4)")?.textContent.trim() ||
        "Không có thông tin giá thấp nhất";
        // Kết hợp các thông tin thành một chuỗi HTML
        const content = `
          <div style="
            position: relative;
            left: -15px;
            bottom: 10px;
            width: 100%;
            font-family: Arial, sans-serif; 
            border: 1px solid #ddd; 
            padding: 20px;
            background-color: #f9f9f9; 
            border-radius: 8px; 
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
          ">
            <!-- Tiêu đề -->
            <h1 style="
              font-size: 20px; 
              color: #333; 
              text-align: center; 
              margin: 0 0 10px;
            ">
              ${projectName} - ${investor}
            </h1>

            <!-- Quận huyện -->
            <p style="
              font-size: 14px; 
              color: #777; 
              text-align: center; 
              margin: 0 0 20px;
            ">
              ${district}
            </p>

            <!-- 3 cột: Số tầng, Số tòa, Mức giá -->
            <div style="display: flex; justify-content: space-between; text-align: center; margin-top: 20px;">
              <!-- Cột 1: Số tầng -->
              <div style="flex: 1;">
                <p style="font-size: 16px; font-weight: bold; margin: 0;">Số căn hộ</p>
                <p style="font-size: 14px; color: #555; margin: 5px 0;">${apartments}</p>
              </div>

              <!-- Cột 2: Số tòa -->
              <div style="flex: 1; border-left: 1px solid #ddd; border-right: 1px solid #ddd; padding: 0 10px;">
                <p style="font-size: 16px; font-weight: bold; margin: 0;">Số tòa</p>
                <p style="font-size: 14px; color: #555; margin: 5px 0;">${buildings}</p>
              </div>

              <!-- Cột 3: Mức giá -->
              <div style="flex: 1;">
                <p style="font-size: 16px; font-weight: bold; margin: 0;">Giá bán</p>
                <p style="font-size: 14px; color: #555; margin: 5px 0;">${minPrice} triệu/m²</p>
              </div>
            </div>
          </div>
        `;
        pro_info.innerHTML = content; // Cập nhật nội dung vào thẻ pro_info

        update_list_chart(
          "project",
          normalizeName(projectName.replace("Tên dự án: ", ""))
        );
        setTimeout(set_Scene(), 1000);
      });
    });
  };
}

export function set_Scene() {
  // Đợi biểu đồ được tạo
  setTimeout(() => {
    console.log("Biểu đồ đã được khởi tạo");

    // Biểu đồ
    const charts = [
      document.getElementById("segment"),
      document.getElementById("history"),
      document.getElementById("type"),
      document.getElementById("correlation"),
    ];

    // Khởi tạo trạng thái
    let currentIndex = 0;
    const totalCharts = charts.length;

    // Thiết lập CSS ban đầu cho các biểu đồ
    charts.forEach((chart, index) => {
      chart.style.transform = `translateX(${index * 100}%)`;
      chart.style.transition = "transform 0.5s";
    });

    comments.forEach((comment, index) => {
      comment.style.transform = `translateX(${index * 150}%)`;
      comment.style.transition = "transform 0.5s";
    });

    // Xử lý sự kiện nút Right
    btnRight.addEventListener("click", () => {
      if (currentIndex < totalCharts - 1) {
        currentIndex++;
        updatePosition();
        updateButtonState();
      }
    });

    // Xử lý sự kiện nút Left
    btnLeft.addEventListener("click", () => {
      if (currentIndex > 0) {
        currentIndex--;
        updatePosition();
        updateButtonState();
      }
    });

    // Hàm cập nhật vị trí biểu đồ
    function updatePosition() {
      charts.forEach((chart, index) => {
        chart.style.transform = `translateX(${(index - currentIndex) * 100}%)`;
      });

      comments.forEach((comment, index) => {
        comment.style.transform = `translateX(${
          (index - currentIndex) * 150
        }%)`;
      });
    }

    // Hàm cập nhật trạng thái nút
    function updateButtonState() {
      btnLeft.style.opacity = currentIndex === 0 ? 0.3 : 1;
      btnLeft.style.cursor = currentIndex === 0 ? "default" : "pointer";
      btnRight.style.opacity = currentIndex === totalCharts - 1 ? 0.3 : 1;
      btnRight.style.cursor =
        currentIndex === totalCharts - 1 ? "default" : "pointer";
    }
    // Cập nhật trạng thái nút ban đầu
    updateButtonState();
  }, 1000);
}

export function set_Event() {
  let project_showed = false;

  eye.addEventListener("click", () => {
    see_deeply();
  });

  // Gắn sự kiện click
  btn_project.addEventListener("click", () => {
    district.style.transition = "transform 0.5s ease"; // Thêm hiệu ứng mượt mà
    lst_project.style.transition = "transform 0.5s ease";

    map_title.style.transition = "opacity 0.5s ease";
    pro_title.style.transition = "opacity 0.5s ease";
    eye.style.transition = "opacity 0.5s ease";

    if (!project_showed) {
      district.style.transform = "translateY(900px)"; // Di chuyển district xuống 100px
      lst_project.style.transform = "translateX(750px)";

      map_title.style.opacity = 0;

      eye.style.opacity = 0;
      eye.style.display = "none";

      pro_title.style.opacity = 1;
      pro_title.style.display = "block";
      project_showed = true;

      pro_info.style.transform = "translateX(0)";
      hideAllComment();
    } else {
      district.style.transform = "translateY(0px)";
      lst_project.style.transform = "translateX(0px)";

      map_title.style.opacity = 1;
      eye.style.opacity = 1;
      eye.style.display = "block";

      pro_title.style.opacity = 0;
      pro_title.style.display = "none";
      project_showed = false;

      update_list_chart("area", "ha_noi");
      set_Scene();

      pro_info.style.transform = "translateX(150%)";
      showAllComment();
    }
  });
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

export function hideComment(cmt_ctn) {
  const container = document.getElementById(cmt_ctn);

  container.style.opacity = 0;
}

export function hideAllComment() {
  comments.forEach((comment) => {
    comment.style.opacity = "0";
  });
}

export function showComment(cmt_cnt) {
  const container = document.getElementById(cmt_cnt);

  container.style.opacity = 1;
}

export function showAllComment() {
  comments.forEach((comment) => {
    comment.style.opacity = "1";
  });
}
