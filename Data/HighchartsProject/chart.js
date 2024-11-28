import {
  handlePieIconClick,
  handleColumnIconClick,
  handleNextIconClick,
  handleBackIconClick,
  toggleCenter,
} from "./events.js";

document.addEventListener("DOMContentLoaded", () => {
  // Fetch và vẽ biểu đồ phân khúc mức giá (Pie Chart)
  fetch("./prices_data.json")
    .then((response) => response.json())
    .then((data) => {
      const { num_price1, num_price2, num_price3, num_price4 } = data;

      // Dữ liệu cho Pie Chart
      const chartData = [
        { name: "Dưới 100 triệu/m²", y: num_price1 },
        { name: "100 đến 200 triệu/m²", y: num_price2 },
        { name: "200 đến 300 triệu/m²", y: num_price3 },
        { name: "Trên 300 triệu/m²", y: num_price4 },
      ];

      // Khởi tạo Pie Chart
      const price_segment = Highcharts.chart("price_segment", {
        chart: {
          type: "pie",
          backgroundColor: null,
        },
        title: {
          text: "Phân khúc mức giá",
          style: {
            color: "white",
            fontSize: "13px",
          },
        },
        tooltip: {
          pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: {
              enabled: true, // Bật hiển thị nhãn
              format: "<b>{point.name}</b>: {point.percentage:.1f} %",
              distance: 30, // Khoảng cách từ tâm đến nhãn
              style: {
                color: "white", // Màu chữ
                textOutline: "none", // Loại bỏ viền chữ
              },
            },
          },
        },
        series: [
          {
            name: "Phần trăm",
            colorByPoint: true,
            data: chartData,
          },
        ],
        exporting: {
          enabled: true,
          buttons: {
            contextButton: {
              align: "right", // Căn phải
              verticalAlign: "top", // Căn đỉnh
              x: 10,
              y: 0,
              symbol: "menu", // Biểu tượng
              menuItems: [
                {
                  text: "beCenter", // Ban đầu là beCenter
                  onclick: function () {
                    const chart_price_segment =
                      document.getElementById("price_segment");
                    toggleCenter(chart_price_segment);
                  },
                },
              ],
            },
          },
        },
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON:", error));

  // Fetch và vẽ biểu đồ biến động giá (Line Chart)
  fetch("./mean_price.json")
    .then((response) => response.json())
    .then((data) => {
      const categories = Object.keys(data[0]).slice(0, -1); // Các tháng
      const lowPrices = Object.values(data[0]).slice(0, -1); // Giá thấp nhất
      const averagePrices = Object.values(data[1]).slice(0, -1); // Giá trung bình
      const highPrices = Object.values(data[2]).slice(0, -1); // Giá cao nhất

      const his_prices = Highcharts.chart("his_prices", {
        chart: {
          type: "line",
          backgroundColor: null,
        },
        title: {
          text: "Biến động giá",
          style: {
            color: "#ffffff",
            fontSize: "13px",
          },
        },
        xAxis: {
          categories: categories.map((key) => key.replace("Giá ", "")),
          title: {
            text: "Thời điểm",
            style: {
              color: "#ffffff",
            },
          },
          labels: {
            enabled: true,
            style: {
              color: "#ffffff",
            },
          },
        },
        yAxis: {
          title: {
            text: "Mức giá",
            style: {
              color: "#ffffff",
            },
          },
          labels: {
            enabled: true,
            style: {
              color: "#ffffff",
            },
          },
        },
        tooltip: {
          shared: false,
          headerFormat: '<span style="font-size: 10px">{point.key}</span><br/>',
          pointFormat:
            '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>',
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          borderColor: "#333333",
          style: {
            color: "#333333",
          },
        },
        plotOptions: {
          series: {
            shadow: true,
          },
        },
        legend: {
          enabled: true,
        },
        series: [
          {
            name: "Max",
            data: highPrices,
            color: "#ff5733",
          },
          {
            name: "Mean",
            data: averagePrices,
            color: "#33b5ff",
          },
          {
            name: "Min",
            data: lowPrices,
            color: "#32cd32",
          },
        ],
        exporting: {
          enabled: true,
          buttons: {
            contextButton: {
              align: "right", // Căn phải
              verticalAlign: "top", // Căn đỉnh
              x: -170,
              y: -10,
              symbol: "./image/icon_next.png", // Biểu tượng
              menuItems: [
                {
                  text: "beCenter", // Ban đầu là beCenter
                  onclick: function () {
                    const chart_hist_prices =
                      document.getElementById("his_prices");
                    toggleCenter(chart_hist_prices);
                  },
                },
              ],
            },
          },
        },
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON:", error));
  // Gọi các hàm sự kiện

  handlePieIconClick();
  handleColumnIconClick();
  handleBackIconClick();
  handleNextIconClick();
});

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


