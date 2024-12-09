const data = [
    {
        IDClass: "History_Pice",
        flavor: "Chart of average price",
        describe: "Biểu đồ này minh họa giá trung bình của các loại hình bất động sản khác nhau tại Hà Nội. Nó cung cấp cái nhìn sâu sắc về xu hướng giá cả và giúp xác định sự khác biệt giữa các loại hình bất động sản.",
        calories: {
            tilte: "Nhà Phố",
            number: 399.2,
            percentage: "Cao Nhất",
        },
        fat: {
            tilte: "Trang Trại",
            number: 25.5,
            percentage: "Thấp Nhất",
        },
        sodium: {
            tilte: "Nhà Riêng",
            number: 200.9,
            percentage: "Phổ Biến",
        },
        carb: {
            tilte: "Chênh lệch",
            number: 72.1,
            percentage: "Ít Nhất",
        },
        protein: {
            tilte: "Chênh lệch",
            number: 373.7,
            percentage: "Cao Nhất",
        },
        chartContainer: '<div id="column_chart_avg_price_of_ha_noi" class="slider-chart"></div>'
    },
    {
        IDClass: "grape",
        flavor: "Bar chart of quantity",
        describe: "Biểu đồ cột này minh họa số lượng các loại hình bất động sản khác nhau tại Hà Nội. Nó làm nổi bật sự phân bố giữa các loại hình, giúp so sánh rõ ràng về mức độ phổ biến của từng loại.",
        calories: {
            tilte: "Nhà Riêng",
            number: 4751,
            percentage: "Cao Nhất",
        },
        fat: {
            tilte: "Nhà Xưởng",
            number: 3,
            percentage: "Thấp Nhất",
        },
        sodium: {
            tilte: "Căn Hộ Chung Cư",
            number: 4115,
            percentage: "Phổ Biến",
        },
        carb: {
            tilte: "Chênh lệch",
            number: 636,
            percentage: "Ít Nhất",
        },
        protein: {
            tilte: "Chênh lệch",
            number: 4738,
            percentage: "Cao Nhất",
        },
        chartContainer: '<div id="column_chart_of_count_classify_of_ha_noi" class="slider-chart"></div>'
    },
    {
        IDClass: "peach",
        flavor: "Heatmap of average prices",
        describe: "Biểu đồ nhiệt này thể hiện giá trung bình của một loại hình bất động sản cụ thể tại các quận huyện ở Hà Nội. Nó làm nổi bật sự chênh lệch giá theo khu vực và giúp xác định các khu vực có xu hướng giá trị thị trường cao hoặc thấp hơn",
        calories: {
            tilte: "Hoàn Kiếm",
            number: 240.1,
            percentage: "Cao Nhất",
        },
        fat: {
            tilte: "Quốc Oai",
            number: 30.4,
            percentage: "Thấp Nhất",
        },
        sodium: {
            tilte: "Tây Hồ",
            number: 96.1,
            percentage: "Phổ Biến",
        },
        carb: {
            tilte: "Chênh lệch",
            number: 135,
            percentage: "Ít Nhất",
        },
        protein: {
            tilte: "Chênh lệch",
            number: 209.7,
            percentage: "Cao Nhất",
        },
        chartContainer: '<iframe id="Average_price_of_type" class="slider-chart" src="heatmap/Average_price_of_type_CC.html" style="width: 100%; height: 100%; border: none;"></iframe>'
    },
    {
        IDClass: "orange",
        flavor: "Heatmap of quantity",
        describe: "Biểu đồ nhiệt này trình bày sự phân bố của một loại hình bất động sản cụ thể tại các quận huyện ở Hà Nội. Nó làm nổi bật các khu vực có mật độ cao và thấp, cung cấp cái nhìn rõ ràng về xu hướng phân bố theo khu vực.",
        calories: {
            tilte: "Nam Từ Liêm",
            number: 1011,
            percentage: "Cao Nhất",
        },
        fat: {
            tilte: "Quốc Oai",
            number: 2,
            percentage: "Thấp Nhất",
        },
        sodium: {
            tilte: "Cầu giấy",
            number: 494,
            percentage: "Phổ Biến",
        },
        carb: {
            tilte: "Chênh lệch",
            number: 517,
            percentage: "Ít Nhất",
        },
        protein: {
            tilte: "Chênh lệch",
            number: 1009,
            percentage: "Cao Nhất",
        },
        chartContainer: '<iframe id="Number_of_types" class="slider-chart" src="heatmap/Number_of_types_CC.html" style="width: 100%; height: 100%; border: none;"></iframe>'
    },
];

const data_Replace =[
    {
        IDClass: "peach",
        flavor: "Heatmap of average prices",
        describe: "This heatmap shows the average prices of a specific real estate type across different districts in Hanoi. It highlights regional price variations and helps identify areas with higher or lower market value trends.",
        calories: {
            tilte: "Cầu Giấy",
            number: 275.1,
            percentage: "Cao Nhất",
        },
        fat: {
            tilte: "Mĩ Đức",
            number: 17.9,
            percentage: "Thấp Nhất",
        },
        sodium: {
            tilte: "Tây Hồ",
            number: 242.3,
            percentage: "Phổ Biến",
        },
        carb: {
            tilte: "Chênh lệch",
            number: 31,
            percentage: "Ít Nhất",
        },
        protein: {
            tilte: "Chênh lệch",
            number: 257.2,
            percentage: "Cao Nhất",
        },
        chartContainer: '<iframe id="Average_price_of_type" class="slider-chart" src="heatmap/Average_price_of_type_CC.html" style="width: 100%; height: 100%; border: none;"></iframe>'
    },
    {
        IDClass: "orange",
        flavor: "Heatmap of quantity",
        describe: "This heatmap showcases the distribution of a specific type of real estate across districts in Hanoi. It highlights areas with high and low concentrations, offering a clear visual of regional patterns.",
        calories: {
            tilte: "Hà Đông",
            number: 603,
            percentage: "Cao Nhất",
        },
        fat: {
            tilte: "Phú Xuyên",
            number: 4,
            percentage: "Thấp Nhất",
        },
        sodium: {
            tilte: "Nam Từ Liêm",
            number: 444,
            percentage: "Phổ Biến",
        },
        carb: {
            tilte: "Chênh lệch",
            number: 35,
            percentage: "Ít Nhất",
        },
        protein: {
            tilte: "Chênh lệch",
            number: 599,
            percentage: "Cao Nhất",
        },
        chartContainer: '<iframe id="Number_of_types" class="slider-chart" src="heatmap/Number_of_types_CC.html" style="width: 100%; height: 100%; border: none;"></iframe>'
    },
];



const container = document.querySelector(".container");
const navigation = container.querySelector(".navigation");
const content = container.querySelector(".content");
const sliderWrapper = container.querySelector(".slider .slider-wrapper");

container.classList.add(`${data[0].IDClass}`);
navigation.innerHTML = "";
content.innerHTML = "";
sliderWrapper.innerHTML = "";

for (let i = 0; i < data.length; i++) {
    navigation.innerHTML += `
        <li class="navigation-item">
            <span></span>
            <span>0${i + 1}</span>
        </li>
    `;
    
    const currentData = data[i];
    if(i <= data.length - 3)
    content.innerHTML += `
        <div class="content-wrapper">
            <h1 class="juice-flavor">${currentData.flavor}</h1>

            <p class="juice-describe">${currentData.describe}</p>

            <div class="juice-nutrition">
                <h4>Parameter</h4>
                <ul class="juice-nutrition-items">
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;" >${currentData.calories.tilte}</span>
                        <span>${currentData.calories.number}</span>
                        <span>${currentData.calories.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;">${currentData.fat.tilte}</span>
                        <span>${currentData.fat.number}</span>
                        <span>${currentData.fat.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;">${currentData.sodium.tilte}</span>
                        <span>${currentData.sodium.number}</span>
                        <span>${currentData.sodium.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;">${currentData.carb.tilte}</span>
                        <span>${currentData.carb.number}</span>
                        <span>${currentData.carb.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;">${currentData.protein.tilte}</span>
                        <span>${currentData.protein.number}</span>
                        <span>${currentData.protein.percentage}</span>
                    </li>
                </ul>
            </div>
            

        </div>
    `;
    else {
        content.innerHTML += `
        <div class="content-wrapper">
            <h1 class="juice-flavor">${currentData.flavor}</h1>

            <p class="juice-describe">${currentData.describe}</p>

            <div class="juice-nutrition">
                <h4>Parameter</h4>
                <ul class="juice-nutrition-items">
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;" id="calories_tilte${i}">${currentData.calories.tilte}</span>
                        <span id="calories_number${i}">${currentData.calories.number}</span>
                        <span id="calories_per${i}">${currentData.calories.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;" id="fat_tilte${i}">${currentData.fat.tilte}</span>
                        <span id="fat_number${i}">${currentData.fat.number}</span>
                        <span id="fat_per${i}">${currentData.fat.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;" id="sodium_tilte${i}">${currentData.sodium.tilte}</span>
                        <span id="sodium_number${i}">${currentData.sodium.number}</span>
                        <span id="sodium_per${i}">${currentData.sodium.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;" id="carb_tilte${i}">${currentData.carb.tilte}</span>
                        <span id="carb_number${i}">${currentData.carb.number}</span>
                        <span id="carb_per${i}">${currentData.carb.percentage}</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span style="font-family:Arial;" id="protein_tilte${i}">${currentData.protein.tilte}</span>
                        <span id="protein_number${i}">${currentData.protein.number}</span>
                        <span id="protein_per${i}">${currentData.protein.percentage}</span>
                    </li>
                </ul>
            </div>
            <div class="radio-inputs">
                <label class="radio">
                    <input type="radio" name="radio_${i}" value="CHCC" checked="">
                    <span class="name">CHCC</span>
                </label>
                <label class="radio">
                    <input type="radio" name="radio_${i}" value="Nha_rieng">
                    <span class="name">Nhà riêng</span>
                </label>
            </div>
        </div>`;
            
    }
    sliderWrapper.innerHTML += `
        <li class="slider-item">
           ${currentData.chartContainer}
        </li>
    `;
}


navigation.children[0].classList.add("active");
content.children[0].classList.add("show");
sliderWrapper.children[0].classList.add("active");

var prevIndex = 0;
var currentIndex = 0;

const handleTransition = (prevIndex, currentIndex) => {
    container.classList.add(`${data[currentIndex].IDClass}`);
    container.classList.remove(`${data[prevIndex].IDClass}`);

    content.children[prevIndex].classList.remove("show");
    content.children[currentIndex].classList.add("show");

    navigation.children[prevIndex].classList.remove("active");
    navigation.children[currentIndex].classList.add("active");

    sliderWrapper.style = `--index: ${currentIndex}`;
}

const prevBtn = container.querySelector(".prev-btn");
const nextBtn = container.querySelector(".next-btn");
prevBtn.disabled = true;
nextBtn.disabled = false;

nextBtn.addEventListener("click", () => {
    prevIndex = currentIndex;
    if(currentIndex < data.length - 1) {
        prevBtn.disabled = false;
        nextBtn.disabled = false;
        currentIndex++;
        sliderWrapper.children[prevIndex].classList.remove("active");
        sliderWrapper.children[currentIndex].classList.add("active");
    }

    if(currentIndex == data.length - 1) {
        nextBtn.disabled = true;
    }

    handleTransition(prevIndex, currentIndex);
});

prevBtn.addEventListener("click", () => {
    prevIndex = currentIndex;
    if(currentIndex > 0) {
        prevBtn.disabled = false;
        nextBtn.disabled = false;
        currentIndex--;
        sliderWrapper.children[prevIndex].classList.remove("active");
        sliderWrapper.children[currentIndex].classList.add("active");
    }

    if(currentIndex == 0) {
        prevBtn.disabled = true;
    }

    handleTransition(prevIndex, currentIndex);
});

// Sự kiện thay đổi cho radio "Average_price_of_type"
document.querySelectorAll('input[name="radio_2"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const averagePriceOfTypeIframe = document.getElementById('Average_price_of_type');
        
        if (averagePriceOfTypeIframe) {
            averagePriceOfTypeIframe.classList.add('hidden'); // Ẩn iframe để tạo hiệu ứng mờ dần
            setTimeout(() => { // Đợi cho hiệu ứng mờ dần hoàn tất trước khi thay đổi src
                if (this.value === 'Nha_rieng' && this.checked) {
                    averagePriceOfTypeIframe.src = 'heatmap/Average_price_of_type_NR.html';
                    updateData(data_Replace[0], 2);
                } else if (this.value === 'CHCC' && this.checked) {
                    averagePriceOfTypeIframe.src = 'heatmap/Average_price_of_type_CC.html';
                    updateData(data[2], 2);
                }
                averagePriceOfTypeIframe.onload = () => { // Khi iframe đã tải xong nội dung mới
                    averagePriceOfTypeIframe.classList.remove('hidden'); // Hiển thị lại iframe với hiệu ứng mờ dần
                };
            }, 500); // Thời gian chờ cho hiệu ứng mờ dần (tương đương với giá trị trong CSS)
        }
    });
});

document.querySelectorAll('input[name="radio_3"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const numberOfTypesIframe = document.getElementById('Number_of_types');
        
        if (numberOfTypesIframe) {
            numberOfTypesIframe.classList.add('hidden'); // Ẩn iframe để tạo hiệu ứng mờ dần
            setTimeout(() => { // Đợi cho hiệu ứng mờ dần hoàn tất trước khi thay đổi src
                if (this.value === 'Nha_rieng' && this.checked) {
                    numberOfTypesIframe.src = 'heatmap/Number_of_types_NR.html';
                    updateData(data_Replace[1], 3);
                } else if (this.value === 'CHCC' && this.checked) {
                    numberOfTypesIframe.src = 'heatmap/Number_of_types_CC.html';
                    updateData(data[3], 3);
                }
                numberOfTypesIframe.onload = () => { // Khi iframe đã tải xong nội dung mới
                    numberOfTypesIframe.classList.remove('hidden'); // Hiển thị lại iframe với hiệu ứng mờ dần
                };
            }, 500); // Thời gian chờ cho hiệu ứng mờ dần (tương đương với giá trị trong CSS)
        }
    });
});

function updateData(data, i) {
    // Helper function to update element with fade effect
    function updateElementWithFade(elementId, newValue) {
        const element = document.getElementById(elementId);
        if (!element) return;  // Check if element exists

        // Fade out
        element.style.transition = "opacity 0.3s ease-in-out"; // Smooth transition
        element.style.opacity = "0";

        // Wait for fade-out effect to complete
        setTimeout(() => {
            element.textContent = newValue; // Update content
            element.style.opacity = "1"; // Fade back in
        }, 300); // Match the duration in CSS
    }

    // Update Calories Information
    updateElementWithFade(`calories_tilte${i}`, data.calories.tilte);
    updateElementWithFade(`calories_number${i}`, data.calories.number);
    updateElementWithFade(`calories_per${i}`, data.calories.percentage);

    // Update Fat Information
    updateElementWithFade(`fat_tilte${i}`, data.fat.tilte);
    updateElementWithFade(`fat_number${i}`, data.fat.number);
    updateElementWithFade(`fat_per${i}`, data.fat.percentage);

    // Update Sodium Information
    updateElementWithFade(`sodium_tilte${i}`, data.sodium.tilte);
    updateElementWithFade(`sodium_number${i}`, data.sodium.number);
    updateElementWithFade(`sodium_per${i}`, data.sodium.percentage);

    // Update Carb Information
    updateElementWithFade(`carb_tilte${i}`, data.carb.tilte);
    updateElementWithFade(`carb_number${i}`, data.carb.number);
    updateElementWithFade(`carb_per${i}`, data.carb.percentage);

    // Update Protein Information
    updateElementWithFade(`protein_tilte${i}`, data.protein.tilte);
    updateElementWithFade(`protein_number${i}`, data.protein.number);
    updateElementWithFade(`protein_per${i}`, data.protein.percentage);
}
