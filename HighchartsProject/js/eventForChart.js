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

    district_map.style.transform = "translateX(-270px) translateY(-300px)";

    // Thay đổi nút
    document.getElementById("eye").innerText = "close";
    
    map_title.innerHTML = 'Khu vực hiện tại: Hà Nội';
  } else {
    ward_map.style.display = "none";
    district_map.style.width = "40%";
    district_map.style.height = "80%";

    district_map.style.transform = "translateX(-49%) translateY(-305px)";

    // Thay đổi nút
    document.getElementById("eye").innerText = "open";
    map_title.style.display = "block";
  }

  // Cập nhật trạng thái
  isDeeplyVisible = !isDeeplyVisible;
}

function update_list_chart(district) {
  makeSegmentPrice("area", district, true, 0, 0, 96.3, 95, "segment");
  makeHistoryPrice("area", district, true, 0, 0, 96.3, 95, "history");
  makeCorrelation("area", district, true, 0, 0, 96.3, 95, "correlation");
  makeNumPropertyType("area", district, true, 0, 0, 96.3, 95, "type");

  set_Scene();
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
        if (isDeeplyVisible) update_list_chart(formattedName);

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

    elements.forEach((element) => {
      element.addEventListener("click", () => {
        // Kiểm tra sự tồn tại của các thẻ con
        const projectNameElement = element.querySelector("h2");
        const projectName = projectNameElement
          ? projectNameElement.textContent.trim()
          : "Tên dự án không có sẵn";

        const viewsElement = element.querySelectorAll("p")[0];
        const views = viewsElement
          ? viewsElement.textContent.trim()
          : "Không có lượt xem";

        const investorElement = element.querySelectorAll("p")[1];
        const investor = investorElement
          ? investorElement.textContent.trim()
          : "Không có thông tin chủ đầu tư";

        const districtElement = element.querySelectorAll("p")[2];
        const district = districtElement
          ? districtElement.textContent.trim()
          : "Không có thông tin quận/huyện";

        const legalStatusElement = element.querySelectorAll("p")[3];
        const legalStatus = legalStatusElement
          ? legalStatusElement.textContent.trim()
          : "Không có thông tin pháp lý";

        const content = `
          <h2 style="display: inline-block; margin-right: 10px; font-size: 20px">${projectName}</h2><br>
          <p style="position: relative; left: 80%">${views}</p>
          <p>${investor}</p>
          <p>${district}</p>
          <p>${legalStatus}</p>
        `;

        pro_info.innerHTML = content; // Cập nhật nội dung vào thẻ pro_info
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

    // Comment
    const comments = [
      document.getElementById("sgm_comment"),
      document.getElementById("fta_comment"),
      document.getElementById("type_comment"),
      document.getElementById("crl_comment"),
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

    eye.addEventListener("click", () => {
      see_deeply();
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
  let eyeClicked = false;

  let project_showed = false;

  eye.addEventListener("click", () => {
    if (!eyeClicked) {
      eyeClicked = true;
    } else {
      eyeClicked = false;
    }
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
    } else {
      district.style.transform = "translateY(0px)";
      lst_project.style.transform = "translateX(0px)";

      map_title.style.opacity = 1;
      eye.style.opacity = 1;
      eye.style.display = "block";

      pro_title.style.opacity = 0;
      pro_title.style.display = "none";
      project_showed = false;

      pro_info.style.transform = "translateX(150%)";
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

export function showComment(cmt_cnt) {
  const container = document.getElementById(cmt_cnt);

  container.style.opacity = 1;
}
