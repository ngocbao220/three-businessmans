document.addEventListener('DOMContentLoaded', () => {
    Highcharts.chart('container', {
      chart: {
        type: 'pie'
      },
      title: {
        text: 'Biểu đồ tròn đơn giản'
      },
      series: [{
        name: 'Tỷ lệ',
        colorByPoint: true,
        data: [
          { name: 'Nhóm A', y: 40 },
          { name: 'Nhóm B', y: 30 },
          { name: 'Nhóm C', y: 20 },
          { name: 'Nhóm D', y: 10 }
        ]
      }]
    });
  });
  