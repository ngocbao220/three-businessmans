document.addEventListener("DOMContentLoaded", () => {
  // Nạp file JSON
  fetch("../../VisualizationData/prices_data.json")
    .then((response) => response.json())
    .then((data) => {
      const { area_name, num_price1, num_price2, num_price3, num_price4 } =
        data;

      // Dữ liệu cho biểu đồ tròn
      const chartData = [
        { name: "Dưới 100", y: num_price1 },
        { name: "Trên 100 và Dưới 200", y: num_price2 },
        { name: "Trên 200 và Dưới 300", y: num_price3 },
        { name: "Trên 300", y: num_price4 },
      ];

      // Tạo biểu đồ tròn
      const pieChart = Highcharts.chart("prices", {
        chart: {
          type: "pie",
          backgroundColor: null,
        },
        title: {
          text: `Phân khúc mức giá tại ${area_name}`,
          style: { color: "white" },
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

      // Hàm hiển thị chi tiết biểu đồ cột
      function showDetails(category) {
        const detailsChart = document.getElementById("details");
        detailsChart.style.display = "block";

        Highcharts.chart("details", {
          chart: {
            type: "column",
            backgroundColor: null,
          },
          title: {
            text: `Chi tiết bất động sản giá ${category}`,
            style: { color: "white" },
          },
          xAxis: {
            title: {
              text: "Danh mục",
              style: { color: "white" },
            },
            categories: ["BĐS 1", "BĐS 2", "BĐS 3"],
            labels: { style: { color: "white" } },
          },
          yAxis: {
            title: {
              text: "Mức giá (triệu)",
              style: { color: "white" },
            },
            labels: { style: { color: "white" } },
          },
          series: [
            {
              name: "Mức giá",
              data: [350, 400, 450], // Dữ liệu mẫu
            },
          ],
        });

        // Hiệu ứng hiển thị chi tiết
        detailsChart.classList.add("show");
      }

      // Nút "Quay về"
      document.getElementById("reset-button").addEventListener("click", () => {
        document.getElementById("prices").style.transform =
          "translateX(0) scale(1)";
        document.getElementById("details").style.display = "none";
        document.getElementById("details").classList.remove("show");
      });

      // Nút "Xem chi tiết"
      document.getElementById("show-button").addEventListener("click", () => {
        document.getElementById("prices").style.transform =
          "translateX(-50%) scale(0.6)";
        document.getElementById("details").classList.add("show");
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON:", error));
});
