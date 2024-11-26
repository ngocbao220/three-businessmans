import {
  handlePieIconClick,
  handleColumnIconClick,
  handleNextIconClick,
  handleBackIconClick,
  toggleCenter,
  no_croll,
} from "./events.js";

document.addEventListener("DOMContentLoaded", () => {
  // Fetch và vẽ biểu đồ phân khúc mức giá (Pie Chart)
  fetch("./Json/Segment_Price/prices_data.json")
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
      Highcharts.chart("price_segment", {
        chart: {
          type: "pie",
          backgroundColor: null,
        },
        title: {
          text: "Phân khúc mức giá",
          style: { color: "white", fontSize: "13px" },
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
    .catch((error) =>
      console.error("Lỗi tải dữ liệu JSON (Pie Chart):", error)
    );

  // Fetch và vẽ biểu đồ biến động giá (Line Chart)
  fetch("./Json/History_Price/area/ha_noi.json")
    .then((response) => response.json())
    .then((jsonData) => {
      const lowPrices = jsonData[0]; // Giá thấp
      const averagePrices = jsonData[1]; // Giá trung bình
      const highPrices = jsonData[2]; // Giá cao

      // Lấy danh sách các tháng
      const categories = Object.keys(lowPrices);

      // Khởi tạo Line Chart
      Highcharts.chart("his_prices", {
        chart: {
          type: "line",
          backgroundColor: null,
        },
        title: {
          text: "Biến động giá",
          style: { color: "#ffffff", fontSize: "13px" },
        },
        xAxis: {
          categories: categories.map((key) => key.replace("Giá ", "")),
          labels: {enabled: true, style: {color: '#ffffff'} },
          plotLines: [
            {
              value: categories.length - 2,
              color: "rgba(255, 255, 255, 0.5)", // Màu đường kẻ
              width: 2, // Độ dày của đường
              dashStyle: "Solid", // Kiểu đường liền
              label: {
                text: "Current",
                align: "center",
                verticalAlign: "top",
                style: {
                  color: "#ffffff",
                  fontSize: "12px",
                },
              },
            },
          ],
        },
        yAxis: {
          labels: { enabled: true, style: {color: "#ffffff"} },
          title: { text: "Triệu/m²", style: {color: '#ffffff', fontSize: '12px'}},
        },
        tooltip: {
          useHTML: true,
          formatter: function () {
            const index = this.point.index;
            return `
            <b>Giá cao nhất:</b> ${highPrices[categories[index]] || "N/A"}<br>
            <b>Giá trung bình:</b> ${
              averagePrices[categories[index]] || "N/A"
            }<br>
            <b>Giá thấp nhất:</b> ${lowPrices[categories[index]] || "N/A"}<br>
          `;
          },
        },
        plotOptions: {
          series: {
            point: {
              events: {
                mouseOver: function () {
                  const chart = this.series.chart;
                  chart.xAxis[0].addPlotLine({
                    id: "hover-line",
                    color: "rgba(255, 255, 255, 0.5)",
                    width: 1,
                    value: this.x,
                  });
                },
                mouseOut: function () {
                  const chart = this.series.chart;
                  chart.xAxis[0].removePlotLine("hover-line");
                },
              },
            },
          },
        },
        series: [
          {
            name: "Max",
            data: Object.values(highPrices), // Lấy giá trị từ object
            color: "#ff5733",
            lineWidth: 2, // Độ dày của đường
            zoneAxis: "x",
            zones: [
              {
                value: Object.keys(highPrices).length - 2 , // Dữ liệu trước prediction
                dashStyle: "Solid",
              },
              {
                dashStyle: "Dash", // Đoạn từ cuối gốc tới prediction
              },
            ],
          },
          {
            name: "Mean",
            data: Object.values(averagePrices),
            color: "#33b5ff",
            lineWidth: 2,
            zoneAxis: "x",
            zones: [
              {
                value: Object.keys(averagePrices).length - 2,
                dashStyle: "Solid",
              },
              {
                dashStyle: "Dash",
              },
            ],
          },
          {
            name: "Min",
            data: Object.values(lowPrices),
            color: "#32cd32",
            lineWidth: 2,
            zoneAxis: "x",
            zones: [
              {
                value: Object.keys(lowPrices).length - 2,
                dashStyle: "Solid",
              },
              {
                dashStyle: "Dash",
              },
            ],
          },
        ],
        legend: {
          enabled: true,
          itemStyle: {
            color: "#f0f0f0",
            fontWeight: "bold",
            fontSize: "13px",
          },
          itemHoverStyle: {
            color: "#ffffff",
          },
          itemHiddenStyle: {
            color: "#999999",
          },
          align: "center",
          verticalAlign: "bottom",
          layout: "horizontal",
        },  
      });
    })
    .catch((error) =>
      console.error("Lỗi tải dữ liệu JSON (Line Chart):", error)
    );

  // Fetch và vẽ biểu đồ tương quan (Heatmap)
  fetch("./Json/Correlation/corr_by_district/corr_by_district.json")
    .then((response) => response.json())
    .then((data) => {
      const categories = data.columns;
      const heatmapData = [];
      data.data.forEach((row, rowIndex) => {
        row.forEach((value, colIndex) => {
          heatmapData.push([rowIndex, colIndex, value]);
        });
      });

      // Khởi tạo Heatmap
      Highcharts.chart("correlation_chart", {
        chart: {
          type: "heatmap",
          marginTop: 40,
          marginBottom: 80,
          plotBorderWidth: 1,
          backgroundColor: null,
        },
        title: {
          text: "Biểu đồ tương quan",
          style: { color: "#ffffff", fontSize: "14px" },
        },
        xAxis: {
          categories: categories,
          labels: { enabled: false, style: { color: "#ffffff" } },
        },
        yAxis: {
          categories: categories,
          labels: { enabled: false, style: { color: "#ffffff" } },
          reversed: true,
        },
        colorAxis: {
          min: -1,
          max: 1,
          stops: [
            [0, "#d4e7ed"],
            [0.5, "#0189bb"],
            [1, "#011a4a"],
          ],
        },
        series: [
          {
            name: "Tương quan",
            borderWidth: 1,
            data: heatmapData,
          },
        ],
        tooltip: {
          formatter: function () {
            return `<b>${categories[this.point.x]} và ${
              categories[this.point.y]
            }</b><br>
              Hệ số tương quan: <b>${this.point.value.toFixed(2)}</b>`;
          },
        },
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON (Heatmap):", error));

  handlePieIconClick();
  handleColumnIconClick();
  handleNextIconClick();
  handleBackIconClick();
  no_croll();
});
