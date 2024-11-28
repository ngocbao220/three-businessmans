import { move, returnToDefalut, typeText, showmore } from "./events.js";

document.addEventListener("DOMContentLoaded", () => {
  // Fetch và vẽ biểu đồ phân khúc mức giá (Pie Chart)
  fetch("../Data/Json/Segment/area/ha_noi.json")
    .then((response) => response.json())
    .then((data) => {
      const {
        under_50,
        between_50_100,
        between_100_150,
        between_150_200,
        over_200,
      } = data;

      // Dữ liệu cho Pie Chart
      const chartData = [
        { name: "Dưới 50 triệu/m²", y: under_50 },
        { name: "50 đến 100 triệu/m²", y: between_50_100 },
        { name: "100 đến 150 triệu/m²", y: between_100_150 },
        { name: "150 đến 200 triệu/m²", y: between_150_200 },
        { name: "Trên 200 triệu/m²", y: over_200 },
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
        exporting: {
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "As The Center",
                  onclick: function () {
                    const chart_price_segment =
                      document.getElementById("price_segment");
                    move(chart_price_segment, -450, 180);
                  },
                },
                "separator",
                {
                  text: "Return To Default",
                  onclick: function () {
                    returnToDefalut();
                  },
                },
                {
                  text: "Show more",
                  onclick: function () {
                    const chart_price_segment =
                      document.getElementById("price_segment");
                    showmore(chart_price_segment, -800, 200, 1.3);
                  },
                },
              ],
            },
          },
        },
      });
    })
    .catch((error) =>
      console.error("Lỗi tải dữ liệu JSON (Pie Chart):", error)
    );
  let count = 0; // Biến đếm số lần click
  let point1 = null; // Lưu giá trị của điểm đầu tiên
  let point2 = null; // Lưu giá trị của điểm thứ hai
  // Fetch và vẽ biểu đồ biến động giá (Line Chart)
  fetch("../Data/Json/History_Price/area/ha_noi.json")
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
          labels: { enabled: true, style: { color: "#ffffff" } },
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
          labels: { enabled: true, style: { color: "#ffffff" } },
          title: {
            text: "Triệu/m²",
            style: { color: "#ffffff", fontSize: "12px" },
          },
        },
        tooltip: {
          useHTML: true,
          formatter: function () {
            const index = this.point.index;
            return `
            <b>Thời điểm:</b> ${categories[index] || "N/A"}<br>
            <b>Giá cao nhất:</b> ${highPrices[categories[index]] || "N/A"}<br>
            <b>Giá trung bình:</b> ${
              averagePrices[categories[index]] || "N/A"
            }<br> 
            <b>Giá thấp nhất:</b> ${lowPrices[categories[index]] || "N/A"}<br>
          `;
          },
          positioner: function (labelWidth) {
            // Đặt tooltip ở góc trên phải của biểu đồ
            return {
              x: this.chart.plotWidth - labelWidth, // Đặt tooltip cách phải 10px
              y: 50, // Đặt tooltip cách trên 10px
            };
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
                click: function () {
                  const index = this.index; // Index of the clicked point
                  const month = categories[index]; // Corresponding month
                  const average = averagePrices[month] || 0; // Average price for the month

                  const defaultRadius = 5; // Default marker size
                  const enlargedRadius = 10; // Enlarged marker size

                  // Toggle marker size
                  if (this.marker && this.marker.radius > defaultRadius) {
                    this.update({
                      marker: {
                        radius: defaultRadius,
                      },
                    });
                    count--; // Decrement click count
                  } else {
                    this.update({
                      marker: {
                        radius: enlargedRadius,
                      },
                    });
                    count++; // Increment click count
                  }

                  // Store the first or second point
                  if (count === 1) {
                    point1 = {
                      month: categories[this.index],
                      index: this.index,
                      value: average,
                    }; // Store the month and index of the first point
                  } else if (count === 2) {
                    point2 = {
                      month: categories[this.index],
                      index: this.index,
                      value: average,
                    }; // Store the month and index of the second point

                    // Calculate the difference in months
                    const difference = point1.value - point2.value;

                    // Display the change in months
                    const textContent = `Biến động giá từ ${point1.month} đến ${
                      point2.month
                    }: ${Math.round(difference * 100) / 100}%.`;

                    typeText("fluctuation", textContent, 20);

                    // Reset selection state
                    count = 0;
                    point1 = null;
                    point2 = null;

                    // Reset all markers to default size
                    const allMarkers = this.series.points;
                    allMarkers.forEach((marker) => {
                      if (marker.graphic) {
                        marker.update({
                          marker: {
                            radius: defaultRadius,
                          },
                        });
                      }
                    });
                  }
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
                value: Object.keys(highPrices).length - 2, // Dữ liệu trước prediction
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
        exporting: {
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "As The Center",
                  onclick: function () {
                    const chart_history_price =
                      document.getElementById("his_prices");
                    move(chart_history_price, -450, -150); // Gọi hàm beCenter và truyền vào container
                  },
                },
                "separator",
                {
                  text: "Return To Default",
                  onclick: function () {
                    returnToDefalut();
                  },
                },
                "separator",
                {
                  text: "Show more",
                  onclick: function () {
                    const chart_history_price =
                      document.getElementById("his_prices");
                    showmore(chart_history_price, -900, -200);
                  },
                },
              ],
            },
          },
        },
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
  fetch("../Data/Json/Correlation/area/ha_noi.json")
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
        exporting: {
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "As The Center",
                  onclick: function () {
                    const chart_correlation =
                      document.getElementById("correlation_chart");
                    move(chart_correlation, 470, -200); // Gọi hàm beCenter và truyền vào container
                  },
                },
                "separator",
                {
                  text: "Return To Default",
                  onclick: function () {
                    returnToDefalut();
                  },
                },
                {
                  text: "Show more",
                  onclick: function () {
                    const chart_correlation =
                      document.getElementById("correlation_chart");
                    showmore(chart_correlation, 0, -200);
                  },
                },
              ],
            },
          },
        },
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON (Heatmap):", error));

  // handlePieIconClick();
  // handleColumnIconClick();
  // handleNextIconClick();
  // handleBackIconClick();
});
