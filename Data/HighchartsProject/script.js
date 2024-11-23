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

      // Vẽ biểu đồ tròn
      Highcharts.chart("prices", {
        chart: {
          type: "pie",
        },
        title: {
          text: `Phân khúc mức giá tại ${area_name}`,
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
                  Highcharts.chart("details", {
                    chart: {
                      type: "column",
                    },
                    title: {
                      text: "Chi tiết bất động sản giá Trên " + this.name,
                    },
                    xAxis: {
                      title: {
                        text: "Danh mục",
                      },
                      categories: ["BĐS 1", "BĐS 2", "BĐS 3"], // Dữ liệu mẫu
                    },
                    yAxis: {
                      title: {
                        text: "Mức giá (triệu)",
                      },
                    },
                    series: [
                      {
                        name: "Mức giá",
                        data: [350, 400, 450], // Dữ liệu mẫu
                      },
                    ],
                  });
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
    });
});
