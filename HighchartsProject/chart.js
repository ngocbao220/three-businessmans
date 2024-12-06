import {
  move,
  returnToDefalut,
  showmore,
  remake_sub_chart_of_Pie,
  remove_sub_chart,
  remake_sub_chart_of_Column,
  show_amount
} from "./events.js";

export function makeSegmentPrice(
  type,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 0,
  height = 0,
  id
) {
  fetch(`../Data/Json/Segment/${type}/${name}.json`)
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

      let chartContainer = document.getElementById(id);
      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.left = `${left}px`;
        chartContainer.style.bottom = `${bottom}px`;
        chartContainer.style.width = `${width}%`;
        chartContainer.style.height = `${height}%`;
        chartContainer.className = "chart";
        document.getElementById("chart-container").appendChild(chartContainer);
      }

      // Khởi tạo Pie Chart
      const chart = Highcharts.chart(id, {
        chart: {
          type: "pie",
          backgroundColor: null,
          events: {
            load: function () {
              this.isShow = false;
            },
          },
        },
        title: {
          text: `Phân khúc mức giá`,
          style: { color: "black", fontSize: "14px" },
        },
        tooltip: {
          pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            events: {
              click: function (event) {
                const clickedName = event.point.name;
                if (chartContainer.isShow == true) {
                  remake_sub_chart_of_Pie(clickedName);
                }
              },
            },
            dataLabels: {
              enabled: true,
              style: {
                color: "black", // Đổi màu chữ nhãn
                fontSize: "12px",
                fontWeight: "bold",
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
          enabled: menu,
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "As The Center",
                  onclick: function () {
                    move(chartContainer, -450, 180);
                  },
                },
                "separator",
                {
                  text: "Return To Default",
                  onclick: function () {
                    returnToDefalut();
                    chartContainer.isShow = false;
                  },
                },
                {
                  text: "Show more",
                  onclick: function () {
                    showmore(chartContainer, -850, 40, 1.2);
                    chartContainer.isShow = true;
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
}

export function makeHistoryPrice(
  type,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 0,
  height = 0,
  id
) {
  let count = 0; // Biến đếm số lần click
  let point1 = null; // Lưu giá trị của điểm đầu tiên
  let point2 = null; // Lưu giá trị của điểm thứ hai
  // Fetch và vẽ biểu đồ biến động giá (Line Chart)
  fetch(`../Data/Json/History_Price/${type}/${name}.json`)
    .then((response) => response.json())
    .then((jsonData) => {
      const lowPrices = jsonData[0]; // Giá thấp
      const averagePrices = jsonData[1]; // Giá trung bình
      const highPrices = jsonData[2]; // Giá cao

      // Lấy danh sách các tháng
      const categories = Object.keys(lowPrices);

      let chartContainer = document.getElementById(id);
      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.left = `${left}px`; // Đặt vị trí từ tham số left
        chartContainer.style.bottom = `${bottom}px`; // Đặt vị trí từ tham số bottom
        chartContainer.style.width = `${width}%`; // Chiều rộng mặc định
        chartContainer.style.height = `${height}%`; // Chiều cao mặc định
        chartContainer.className = "chart";
        document.getElementById("chart-container").appendChild(chartContainer);
      }

      // Khởi tạo Line Chart
      Highcharts.chart(id, {
        chart: {
          type: "line",
          backgroundColor: null,
          events: {
            load: function () {
              this.isShow = false;
            },
          },
        },
        title: {
          text: "Biến động giá",
          style: { color: "#000000", fontSize: "16px" },
        },
        xAxis: {
          categories: categories.map((key) => key.replace("Giá ", "")),
          labels: { enabled: true, style: { color: "#000000" } },
          gridLineColor: "#cccccc", // Màu của đường kẻ dọc
          gridLineWidth: 1, // Độ dày của đường kẻ
          plotLines: [
            {
              value: categories.length - 2,
              color: "#000", // Màu đường kẻ
              width: 2, // Độ dày của đường
              dashStyle: "Solid", // Kiểu đường liền
              label: {
                text: "Current",
                align: "center solid",
                verticalAlign: "top",
                style: {
                  color: "#000000",
                  fontSize: "13px",
                },
              },
            },
          ],
        },
        yAxis: {
          labels: { enabled: true, style: { color: "#000000" } },
          title: {
            text: "Triệu/m²",
            style: { color: "#000000", fontSize: "12px" },
          },
          gridLineColor: "#cccccc", // Màu của đường kẻ ngang
          gridLineWidth: 1, // Độ dày của đường kẻ
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
          positioner: function () {
            // Đặt tooltip ở góc trên phải của biểu đồ
            return {
              x: 10, // Đặt tooltip cách phải 10px
              y: 0, // Đặt tooltip cách trên 10px
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
                    color: "black",
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
                  const value = this.y;

                  const defaultRadius = 4; // Default marker size
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
                      value: value,
                    }; // Store the month and index of the first point
                  } else if (count === 2) {
                    point2 = {
                      month: categories[this.index],
                      index: this.index,
                      value: value,
                    }; // Store the month and index of the second point

                    // Calculate the difference in months
                    const difference = (point2.value / point1.value - 1) * 100;

                    // Display the change in months
                    const textContent = `${point1.month} đến ${
                      point2.month
                    }: ${Math.round(difference * 100) / 100}% `;

                    show_amount("fluctuation", textContent, difference);

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
          enabled: menu,
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "As The Center",
                  onclick: function () {
                    move(chartContainer, -450, -150); // Gọi hàm beCenter và truyền vào container
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
                    showmore(chartContainer, -880, -200, 1.3);
                    chartContainer.isShow = true;
                    const fluctuationIn2Years =
                      Math.round(
                        (averagePrices[categories[24]] /
                          averagePrices[categories[0]] -
                          1) *
                          10000
                      ) / 100;
                    const meanOfFluctuation =
                      Math.round(fluctuationIn2Years * 4) / 100;

                    const fluctuationIn2YearsText = `Giá Bất động sản tại khu vực Hà Nội đã tăng ${fluctuationIn2Years} % trong 2 năm qua!`;
                    const meanOfFluctuationText = `Mức tăng trung bình ${meanOfFluctuation} % trên tháng`;

                    typeText(
                      "fluctuationIn2Years",
                      fluctuationIn2YearsText,
                      20,
                      4000
                    );
                    typeText(
                      "meanOfFluctuation",
                      meanOfFluctuationText,
                      20,
                      4000
                    );
                  },
                },
              ],
            },
          },
        },
        legend: {
          enabled: true,
          itemStyle: {
            color: "#000",
            fontWeight: "bold",
            fontSize: "13px",
          },
          itemHoverStyle: {
            color: "#000",
          },
          itemHiddenStyle: {
            color: "#000",
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
}

export function makeCorrelation(
  type,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 0,
  height = 0,
  className
) {
  fetch(`../Data/Json/Correlation/${type}/${name}.json`)
    .then((response) => response.json())
    .then((data) => {
      const categories = data.columns;
      const heatmapData = [];
      data.data.forEach((row, rowIndex) => {
        row.forEach((value, colIndex) => {
          heatmapData.push([rowIndex, colIndex, value]);
        });
      });

      const id = `correlation_of_${name}`;
      let chartContainer = document.getElementById(id);

      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.left = `${left}px`;
        chartContainer.style.bottom = `${bottom}px`;
        chartContainer.style.width = `${width}%`;
        chartContainer.style.height = `${height}%`;
        chartContainer.classList.add(className);
        chartContainer.style.opacity = "0";

        document.body.appendChild(chartContainer);

        requestAnimationFrame(() => {
          chartContainer.style.opacity = "1"; // Sáng dần lên
        });
      }

      // Khởi tạo Heatmap
      Highcharts.chart(id, {
        chart: {
          type: "heatmap",
          marginTop: 50,
          marginBottom: 140,
          plotBorderWidth: 2,
          backgroundColor: null,
        },
        title: {
          text: "Biểu đồ tương quan",
          align: "center",
          style: { color: "#ffffff", fontSize: "16px" },
        },
        xAxis: {
          categories: categories,
          title: null,
          labels: { style: { color: "#ffffff" } },
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
            [0, "#fee5d9"],
            [0.5, "#fcae91"],
            [1, "#fb6a4a"],
          ],
          layout: "horizontal", // Đặt thanh màu dọc
          align: "center", // Đặt bên phải vùng vẽ biểu đồ
          x: 20, // Dịch thanh màu ra ngoài vùng vẽ
          y: 0, // Không dịch theo chiều dọc
          symbolHeight: 200, // Chiều cao của thanh màu
        },
        series: [
          {
            name: "Tương quan",
            borderWidth: 1,
            data: heatmapData,
            dataLabels: {
              enabled: true,
              color: "#000000",
              formatter: function () {
                return this.point.value.toFixed(2);
              },
            },
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
          enabled: menu,
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "As The Center",
                  onclick: function () {
                    const chart_correlation = document.getElementById(id);
                    move(chart_correlation, 470, -200);
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
                    const chart_correlation = document.getElementById(id);
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
}

export function makeSegmentCount(
  type,
  pricetype,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 0,
  height = 0,
  className
) {
  // Lấy dữ liệu từ tệp JSON
  fetch(`../Data/Json/Segment/${type}/count/${pricetype}/${name}.json`)
    .then((response) => response.json())
    .then((data) => {
      const chartData = Object.keys(data).map((key) => ({
        name: key,
        y: data[key],
      }));

      const id = `donut_chart_of_${name}`;

      // Kiểm tra và tạo thẻ div cho biểu đồ nếu chưa có
      let chartContainer = document.getElementById(id);
      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.left = `${left}px`; // Đặt vị trí từ tham số left
        chartContainer.style.bottom = `${bottom}px`; // Đặt vị trí từ tham số bottom
        chartContainer.style.width = `${width}%`; // Chiều rộng mặc định
        chartContainer.style.height = `${height}%`; // Chiều cao mặc định
        chartContainer.className = className;
        document.body.appendChild(chartContainer);
      }

      // Khởi tạo biểu đồ hình bánh donut
      Highcharts.chart(id, {
        chart: {
          type: "pie", // Loại biểu đồ pie
          backgroundColor: null,
        },
        title: {
          text: `Phân khúc Bất động sản `,
          style: { color: "white", fontSize: "13px" },
        },
        tooltip: {
          pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
        },
        plotOptions: {
          pie: {
            innerSize: "50%", // Tạo hình donut bằng cách thiết lập innerSize
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: {
              enabled: true,
              format: "{point.name}: {point.y}", // Hiển thị tên và giá trị khi hover
            },
          },
        },
        series: [
          {
            name: "Phân khúc",
            colorByPoint: true,
            data: chartData,
          },
        ],
        exporting: {
          enabled: menu,
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "As The Center",
                  onclick: function () {
                    move(chartContainer, +450, 180);
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
                    showmore(chartContainer, -800, 200, 1.3);
                  },
                },
              ],
            },
          },
        },
      });
    })
    .catch((error) =>
      console.error("Lỗi tải dữ liệu JSON (Donut Chart):", error)
    );
}

export function makeNumPropertyType(
  type,
  name,
  menu = false,
  left = 900,
  bottom = 0,
  width = 0,
  height = 0,
  className
) {
  // Lấy dữ liệu từ tệp JSON
  fetch(`../Data/Json/Number_Of_Type_Property/${type}/${name}.json`)
    .then((response) => response.json())
    .then((data) => {
      const categories = Object.keys(data); // Các loại bất động sản
      const values = Object.values(data); // Số lượng tương ứng

      const id = `column_chart_of_count_classify_of_${name}`;

      let chartContainer = document.getElementById(id);

      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.left = `${left}px`; // Vị trí từ tham số left
        chartContainer.style.bottom = `${bottom}px`; // Vị trí từ tham số bottom
        chartContainer.style.width = `${width}%`; // Chiều rộng
        chartContainer.style.height = `${height}%`; // Chiều cao
        chartContainer.className = className;
        document.body.appendChild(chartContainer);
      }

      // Khởi tạo biểu đồ cột
      Highcharts.chart(id, {
        chart: {
          type: "column", // Biểu đồ dạng cột
          backgroundColor: null,
          events: {
            load: function () {
              this.isShow = false;
            },
          },
        },
        title: {
          text: `Biểu đồ số lượng bất động sản theo loại hình`,
          style: { color: "white", fontSize: "13px" },
        },
        xAxis: {
          categories: categories, // Các loại bất động sản (trục X)
          title: {
            text: "Loại bất động sản",
            style: { color: "white", fontSize: "13px", align: "center" },
          },
          labels: {
            enabled: false,
          },
        },
        yAxis: {
          min: 0,
          title: {
            text: "Số lượng",
            style: { color: "white", fontSize: "13px" },
          },
        },
        plotOptions: {
          column: {
            cursor: "pointer",
            events: {
              click: function (event) {
                const clickedName = event.point.category;
                if (chartContainer.isShow == true) {
                  remake_sub_chart_of_Column(clickedName);
                }
              },
            },
          },
        },
        series: [
          {
            name: "Số lượng",
            data: values, // Dữ liệu của biểu đồ cột
            colorByPoint: true,
          },
        ],
        exporting: {
          enabled: menu,
          buttons: {
            contextButton: {
              menuItems: [
                {
                  text: "Di chuyển ra giữa ",
                  onclick: function () {
                    move(chartContainer, +450, 180);
                  },
                },
                "separator",
                {
                  text: "Quay lại mặc định",
                  onclick: function () {
                    returnToDefalut();
                    chartContainer.isShow = false;
                  },
                },
                {
                  text: "Hiển thị thêm",
                  onclick: function () {
                    showmore(chartContainer, 50, 0, 1.3);
                    chartContainer.isShow = true;
                  },
                },
              ],
            },
          },
        },
      });
    })
    .catch((error) =>
      console.error("Lỗi tải dữ liệu JSON (Column Chart):", error)
    );
}

export function makeAveragePriceChart(
  type,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 0,
  height = 0,
  className
) {
  fetch(`../Data/Json/Mean_Price//${type}/${name}.json`)
    .then((response) => response.json())
    .then((data) => {
      const categories = Object.keys(data); // Các loại bất động sản
      const values = Object.values(data); // Giá trung bình

      const id = `column_chart_avg_price_of_${name}`;

      // Kiểm tra và tạo thẻ div cho biểu đồ nếu chưa có
      let chartContainer = document.getElementById(id);
      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.left = `${left}px`;
        chartContainer.style.bottom = `${bottom}px`;
        chartContainer.style.width = `${width}%`;
        chartContainer.style.height = `${height}%`;
        chartContainer.className = className;
        document.body.appendChild(chartContainer);
      }

      // Khởi tạo biểu đồ cột
      Highcharts.chart(id, {
        chart: {
          type: "column",
          backgroundColor: null,
        },
        title: {
          text: `Biểu đồ giá trung bình theo loại hình bất động sản`,
          style: { color: "white", fontSize: "16px" },
        },
        xAxis: {
          categories: categories,
          title: {
            text: "Loại bất động sản",
            style: { color: "white", fontSize: "13px" },
          },
          labels: {
            enabled: false,
          },
        },
        yAxis: {
          min: 0,
          title: {
            text: "Giá trung bình (triệu đồng)",
            style: { color: "white", fontSize: "13px" },
          },
        },
        series: [
          {
            name: "Giá trung bình",
            data: values,
            colorByPoint: true,
          },
        ],
        exporting: {
          enabled: menu,
        },
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON:", error));
}
