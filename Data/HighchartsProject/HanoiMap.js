// Xử lý sự kiện khi click vào quận/huyện trong iframe bản đồ
document.addEventListener('DOMContentLoaded', () => {
    const iframe = document.querySelector('.map-container iframe');
    iframe.addEventListener('load', () => {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        
        const layers = Object.keys(iframe.contentWindow); // Tìm tất cả các lớp trong iFrame
        layers.forEach(layerKey => {
            const layer = iframe.contentWindow[layerKey];
            if (layer instanceof iframe.contentWindow.L.GeoJSON) {
                layer.eachLayer(function (featureLayer) {
                    featureLayer.on('click', function () {
                        // Thay đổi kích thước biểu đồ
                        const chartDiv = document.getElementById('his_prices');
                        if (chartDiv) {
                            chartDiv.style.transition = "all 0.5s"; // Hiệu ứng mượt
                            chartDiv.style.width = "80%";
                            chartDiv.style.height = "400px";

                            // Gọi cập nhật nội dung biểu đồ từ file chart.js
                            import('./chart.js').then((chart) => {
                                chart.updateChart(featureLayer.feature.properties);
                            });
                        }
                    });
                });
            }
        });
    });
});
