document.addEventListener("DOMContentLoaded", () => {
  fetch("./prices_data.json")
    .then((response) => response.json())
    .then((data) => {
      const { area_name, num_price1, num_price2, num_price3, num_price4 } =
        data;
      // Dữ liệu
      const chartData = [
        { name: "Dưới 100 triệu/m²", y: num_price1 },
        { name: "100 đến 200 triệu/m²", y: num_price2 },
        { name: "200 đến 300 triệu/m²", y: num_price3 },
        { name: "Trên 300 triệu/m²", y: num_price4 },
      ];

      // Tạo biểu đồ tròn
      const pieChart = Highcharts.chart("price_segment", {
        chart: {
          type: "pie",
          backgroundColor: null,
        },
        title: {
          text: `Phân khúc mức giá`,
          style: {
            color: "white",
            fontSize: "16px",
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
              enabled: true,
              format: "<b>{point.name}</b>: {point.percentage:.1f} %",
            },
            point: {
              events: {
                click: function () {
                  showDetails(this.name);
                  // Hiệu ứng dịch biểu đồ tròn
                  document.getElementById("prices").style.transform =
                    "translateX(-50%) scale(0.6)";
                },
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

  fetch("mean_price.json") // Đường dẫn tới file JSON
    .then((response) => response.json())
    .then((data) => {
      // Chuẩn bị dữ liệu cho biểu đồ
      const area_name = Object.values(data[0]).slice(-1)[0];
      const categories = Object.keys(data[0]).slice(0, -1); // Các tháng từ dữ liệu JSON
      const lowPrices = Object.values(data[0]).slice(0, -1); // Giá thấp nhất
      const averagePrices = Object.values(data[1]).slice(0, -1); // Giá trung bình
      const highPrices = Object.values(data[2]).slice(0, -1); // Giá cao nhất

      // Vẽ biểu đồ đường
      Highcharts.chart("his_prices", {
        chart: {
          type: "line",
          backgroundColor: null, // Nền tối
        },
        title: {
          text: "Biến động giá bất động sản",
          style: {
            color: "#ffffff", // Màu chữ
            fontSize: "18px",
          },
        },
        xAxis: {
          categories: categories.map((key) => key.replace("Giá ", "")), // Loại bỏ tiền tố "Giá "
          title: {
            text: "Thời gian",
            style: {
              color: "#ffffff",
            },
          },
          labels: {
            style: {
              color: "#ffffff", // Màu nhãn
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
            style: {
              color: "#ffffff",
            },
          },
        },
        legend: {
          itemStyle: {
            color: "#ffffff",
          },
        },
        tooltip: {
          shared: true, // Hiển thị tooltip chung cho tất cả các series
          crosshairs: true, // Thêm crosshair khi hover
          formatter: function () {
            let tooltipText = `<b>${this.x}</b><br/>`; // Thêm thông tin x (tháng)
            this.points.forEach((point) => {
              tooltipText += `<span style="color:${point.color}">\u25CF</span> ${point.series.name}: ${point.y} triệu/m²<br/>`;
            });
            return tooltipText;
          },
        },
        series: [
          {
            name: "Max",
            data: highPrices,
            color: "#dc3545",
          },
          {
            name: "Mean",
            data: averagePrices,
            color: "#007bff",
          },
          {
            name: "Min",
            data: lowPrices,
            color: "#28a745",
          },
        ],
      });
    })
    .catch((error) => console.error("Lỗi khi tải file JSON:", error));
});
