import {
  move,
  returnToDefalut,
  remake_sub_chart_of_Pie,
  remove_sub_chart,
  remake_sub_chart_of_Column,
  show_amount
} from "./events.js";

export function makeCorrelation(
  type,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 0,
  height = 0
) {
  // Fetch và vẽ biểu đồ tương quan (Heatmap)
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
      }
      // Khởi tạo Heatmap
      Highcharts.chart(id, {
        chart: {
          type: "heatmap",
          marginTop: 50,
          marginBottom: 140,
          plotBorderWidth: 2,
          backgroundColor: null,
          // Đặt kích thước của biểu đồ tại đây
          width: 900,  // Thay đổi chiều rộng
          height: 600,  // Thay đổi chiều cao
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
            return `<b>${categories[this.point.x]} và ${categories[this.point.y]}</b><br>
              Hệ số tương quan: <b>${this.point.value.toFixed(2)}</b>`;
          },
        },
        exporting: {
          enabled: false,
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
          enabled: false,
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
          enabled: false,
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
          enabled: false,
        },
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu JSON:", error));
}

export function makeStdDevChart(
  type,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 100, // mặc định 100% chiều rộng
  height = 60  // mặc định 60% chiều cao
) {
  const stddevPath = `../Data/Json/Std_And_Variance/Std/${type}/${name}.json`;

  fetch(stddevPath)
    .then((response) => response.json())
    .then((stddevData) => {
      console.log("Dữ liệu độ lệch chuẩn được tải thành công:", stddevData);

      const categories = Object.keys(stddevData);
      const stddevSeries = Object.values(stddevData);

      const id = `stddev_chart_${name}`;

      // Tạo thẻ chứa biểu đồ nếu chưa tồn tại
      let chartContainer = document.getElementById(id);
      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.position = "absolute";
        chartContainer.style.left = `${left}px`;
        chartContainer.style.bottom = `${bottom}px`;
        chartContainer.style.width = `${width}%`;
        chartContainer.style.height = `${height}%`;
        document.body.appendChild(chartContainer);
      }

      // Vẽ biểu đồ
      Highcharts.chart(id, {
        chart: {
          type: "column",
          backgroundColor: null,
        },
        title: {
          text: `Biểu đồ Độ Lệch Chuẩn (${name})`,
          style: { color: "white", fontSize: "16px" },
        },
        xAxis: {
          categories: categories,
          title: {
            text: "Tháng",
            style: { color: "white", fontSize: "13px" },
          },
        },
        yAxis: {
          min: 0,
          title: {
            text: "Độ Lệch Chuẩn",
            style: { color: "white", fontSize: "13px" },
          },
        },
        series: [
          {
            name: "Độ lệch chuẩn",
            data: stddevSeries,
            color: "#434348",
          },
        ],
        exporting: {
          enabled: menu,
        },
      });
    })
    .catch((error) => console.error("Lỗi tải dữ liệu độ lệch chuẩn:", error));
}

export function makeVarianceChart(
  type,
  name,
  menu = false,
  left = 0,
  bottom = 0,
  width = 100, // mặc định 100% chiều rộng
  height = 60  // mặc định 60% chiều cao
) {
  const variancePath = `../Data/Json/Std_And_Variance/Variance/${type}/${name}.json`;

  fetch(variancePath)
    .then((response) => response.json())
    .then((varianceData) => {
      console.log("Dữ liệu phương sai được tải thành công:", varianceData);

      const categories = Object.keys(varianceData);  // Danh sách các tháng
      const varianceSeries = Object.values(varianceData);  // Giá trị phương sai

      const id = `variance_chart_${name}`;

      // Tạo thẻ chứa biểu đồ nếu chưa tồn tại
      let chartContainer = document.getElementById(id);
      if (!chartContainer) {
        chartContainer = document.createElement("div");
        chartContainer.id = id;
        chartContainer.style.position = "absolute";
        chartContainer.style.left = `${left}px`;
        chartContainer.style.bottom = `${bottom}px`;
        chartContainer.style.width = `${width}%`;
        chartContainer.style.height = `${height}%`;
        document.body.appendChild(chartContainer);
      }

      // Vẽ biểu đồ cột
      Highcharts.chart(id, {
        chart: {
          type: 'column',
          backgroundColor: null,  // Không có nền
        },
        title: {
          text: 'Biểu đồ phương sai theo tháng',
          style: { color: 'white', fontSize: '16px' },
        },
        xAxis: {
          categories: categories,
          title: {
            text: 'Tháng',
            style: { color: 'white', fontSize: '13px' },
          },
        },
        yAxis: {
          min: 0,
          title: {
            text: 'Giá trị',
            style: { color: 'white', fontSize: '13px' },
          },
        },
        tooltip: {
          headerFormat: "<b>{point.x}</b><br/>",
          pointFormat: "{series.name}: {point.y}",
        },
        series: [{
          name: 'Giá trị phương sai',
          data: varianceSeries,
          color: '#7cb5ec',  // Màu cho cột
        }],
        credits: {
          enabled: menu,  // Nếu muốn tắt credits thì set là false
        },
      });
    })
    .catch((error) => console.error('Lỗi khi tải dữ liệu JSON:', error));
}
