

// Xử lý sự kiện khi di chuột vào quận/huyện
document.addEventListener('DOMContentLoaded', () => {
  const iframes = document.querySelectorAll('.map iframe'); // Lấy tất cả các iframe trong .map-container

  iframes.forEach(iframe => {
    iframe.addEventListener('load', () => {
      const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

      // Lặp qua các lớp trong iframe
      const layers = Object.keys(iframe.contentWindow); // Tìm tất cả các lớp trong iFrame
      layers.forEach(layerKey => {
        const layer = iframe.contentWindow[layerKey];
        if (layer instanceof iframe.contentWindow.L.GeoJSON) {
          layer.eachLayer(function (featureLayer) {
            // Lưu lại phong cách ban đầu của mỗi quận/huyện

            // Hiệu ứng khi di chuột vào
            featureLayer.on('mouseover', function () {
              // Nhô quận/huyện hiện tại lên 2px
              featureLayer.setStyle({
                fillOpacity: 1,
                weight: 2,
              });

              // Thêm hiệu ứng di chuyển theo trục Y bằng CSS
              const targetPath = featureLayer._path;
              if (targetPath) {
                targetPath.style.transition = "transform 0.3s ease";
                targetPath.style.transform = "translateY(-6px)";
              }

              // Làm mờ các quận/huyện khác
              layer.eachLayer(function (otherLayer) {
                if (otherLayer !== featureLayer) {
                  otherLayer.setStyle({
                    fillOpacity: 0.5,
                  });
                }
              });
            });

            // Hiệu ứng khi di chuột ra ngoài
            featureLayer.on('mouseout', function () {
              // Đặt lại hiệu ứng di chuyển
              const targetPath = featureLayer._path;
              if (targetPath) {
                targetPath.style.transition = "transform 0.3s ease";
                targetPath.style.transform = "translateY(0px)";
              }

              // Khôi phục lại phong cách cho tất cả các quận/huyện
              layer.eachLayer(function (resetLayer) {
                resetLayer.setStyle({
                  fillOpacity: 0.6,
                  weight: 1,
                  color: 'black', // Đường viền mặc định
                });
              });
            });
          });
        }
      });
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // Truy cập vào các thẻ container
  const mapContainer = document.querySelector('.map-container');
  const xaphuongContainer = document.querySelector('.xaphuong-container');
  const xaphuongIframe = document.querySelector('.xaphuong'); // Iframe hiển thị xã/phường

  // Lắng nghe khi iframe bản đồ đã tải
  const iframe = document.querySelector(".Hanoimap");
  iframe.addEventListener("load", () => {
    const layers = Object.keys(iframe.contentWindow);

    // Tìm các lớp (layers) trong bản đồ
    layers.forEach(layerKey => {
      const layer = iframe.contentWindow[layerKey];

      if (layer instanceof iframe.contentWindow.L.GeoJSON) {
        // Duyệt từng quận/huyện
        layer.eachLayer(featureLayer => {
          featureLayer.on("click", () => {
            // Lấy tên quận/huyện từ thuộc tính của GeoJSON
            const districtName = featureLayer.feature.properties.NAME_2;
            const formattedName = districtName.replace(/\s/g, "_"); // Thay khoảng trắng bằng gạch dưới
            const newSrc = `heatmap/${formattedName}.html`;
            xaphuongIframe.src = newSrc;
            
            // Thêm class để kích hoạt hiệu ứng
            
             xaphuongIframe.onload = () => {
               console.log(`Iframe loaded: ${newSrc}`);
             };
           
            mapContainer.classList.add("slide-bck-tl");
            xaphuongContainer.classList.add("scale-up-center");
            
          });
        });
      }
    });
  });
});


