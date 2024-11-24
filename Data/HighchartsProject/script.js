document.addEventListener("DOMContentLoaded", () => {
  fetch("./prices_data.json")
    .then((response) => response.json())
    .then((data) => {
      const { num_price1, num_price2, num_price3, num_price4 } = data;

      // Dữ liệu
      const chartData = [
        { name: "Dưới 100 triệu/m²", y: num_price1 },
        { name: "100 đến 200 triệu/m²", y: num_price2 },
        { name: "200 đến 300 triệu/m²", y: num_price3 },
        { name: "Trên 300 triệu/m²", y: num_price4 },
      ];

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
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON:", error));

  // Fetch và vẽ biểu đồ biến động giá
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
            shadow: true, // Thêm bóng đổ cho các đường
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
      });
    })
    .catch((error) => console.error("Lỗi khi tải file JSON:", error));

  document.getElementById("pie_icon").addEventListener("click", function () {
    if (this.style.opacity === "0.5") {
      this.style.opacity = "1";
      price_segment.style.opacity = 1;
    } else {
      this.style.opacity = "0.5";
      price_segment.style.opacity = 0;
    }
  });
  document.getElementById("column_icon").addEventListener("click", function () {
    if (this.style.opacity === "0.5") {
      this.style.opacity = "1";
      his_prices.style.opacity = 1;
    } else {
      this.style.opacity = "0.5";
      his_prices.style.opacity = 0;
    }
  });
});
