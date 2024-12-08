const data = [
    {
        flavor: "History_Pice",
        describe: ".......",
        calories: {
            number: 140,
            percentage: 6,
        },
        fat: {
            number: 140,
            percentage: 6,
        },
        sodium: {
            number: 140,
            percentage: 6,
        },
        carb: {
            number: 140,
            percentage: 6,
        },
        protein: {
            number: 140,
            percentage: 6,
        },
        chartContainer: '<div id="column_chart_avg_price_of_ha_noi" class="slider-chart"></div>'
    },
    {
        flavor: "grape",
        describe: "super very unbelievable, siu ngon từ hương vị",
        calories: {
            number: 140,
            percentage: 6,
        },
        fat: {
            number: 140,
            percentage: 6,
        },
        sodium: {
            number: 140,
            percentage: 6,
        },
        carb: {
            number: 140,
            percentage: 6,
        },
        protein: {
            number: 140,
            percentage: 6,
        },
        chartContainer: '<div id="column_chart_of_count_classify_of_ha_noi" class="slider-chart"></div>'
    },
    {
        flavor: "orange",
        describe: "super very unbelievable, siu ngon từ hương vị",
        calories: {
            number: 140,
            percentage: 6,
        },
        fat: {
            number: 140,
            percentage: 6,
        },
        sodium: {
            number: 140,
            percentage: 6,
        },
        carb: {
            number: 140,
            percentage: 6,
        },
        protein: {
            number: 140,
            percentage: 6,
        },
        chartContainer: '<iframe class="slider-chart" src="heatmap/lNumber_of _types.html" style="width: 100%; height: 100%; border: none;"></iframe>'
    },
    {
        flavor: "peach",
        describe: "super very unbelievable, siu ngon từ hương vị",
        calories: {
            number: 140,
            percentage: 6,
        },
        fat: {
            number: 140,
            percentage: 6,
        },
        sodium: {
            number: 140,
            percentage: 6,
        },
        carb: {
            number: 140,
            percentage: 6,
        },
        protein: {
            number: 140,
            percentage: 6,
        },
        chartContainer: '<iframe class="slider-chart" src="heatmap/Average_price_of_type.html" style="width: 100%; height: 100%; border: none;"></iframe>'
    },
];


const container = document.querySelector(".container");
const navigation = container.querySelector(".navigation");
const content = container.querySelector(".content");
const sliderWrapper = container.querySelector(".slider .slider-wrapper");

container.classList.add(`${data[0].flavor}`);
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
    content.innerHTML += `
        <div class="content-wrapper">
            <h1 class="juice-flavor">${currentData.flavor}</h1>

            <p class="juice-describe">${currentData.describe}</p>

            <div class="juice-nutrition">
                <h4>Nutrition Facts</h4>
                <ul class="juice-nutrition-items">
                    <li class="juice-nutrition-item">
                        <span>Calories</span>
                        <span>${currentData.calories.number}</span>
                        <span>${currentData.calories.percentage}%</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span>Total fat</span>
                        <span>${currentData.fat.number}</span>
                        <span>${currentData.fat.percentage}%</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span>Sodium</span>
                        <span>${currentData.sodium.number}</span>
                        <span>${currentData.sodium.percentage}%</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span>Total Carb</span>
                        <span>${currentData.carb.number}</span>
                        <span>${currentData.carb.percentage}%</span>
                    </li>
                    <li class="juice-nutrition-item">
                        <span>Protein</span>
                        <span>${currentData.protein.number}</span>
                        <span>${currentData.protein.percentage}%</span>
                    </li>
                </ul>
            </div>
            <div class="add-to-cart">
                <div class="add-to-cart-btn">
                    <span>price segment</span>
                    <span class="cart-icon">
                        <i class="fa-solid fa-chevron-down"></i>
                    </span>
                </div>
                <span class="heart">
                    <i class="fa-regular fa-heart"></i>
                </span>
            </div>
            <div class="radio-inputs" style="display: none;">
                <label class="radio">
                    <input type="radio" name="radio" value="CHCC" checked="">
                    <span class="name">CHCC</span>
                </label>
                <label class="radio">
                    <input type="radio" name="radio" value="Nha_rieng">
                    <span class="name">Nhà riêng</span>
                </label>
                <label class="radio">
                    <input type="radio" name="radio" value="vu">
                    <span class="name">Vu</span>
                </label>
            </div>

        </div>
    `;
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
    container.classList.add(`${data[currentIndex].flavor}`);
    container.classList.remove(`${data[prevIndex].flavor}`);

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

const addToCartBtn = document.querySelector('.add-to-cart-btn');
const radioInputs = document.querySelector('.radio-inputs');

// Xử lý khi click vào add-to-cart-btn
addToCartBtn.addEventListener('click', function () {
    if (radioInputs.style.display === 'none' || radioInputs.style.display === '') {
        radioInputs.style.display = 'block';
    } else {
        radioInputs.style.display = 'none';
    }
});

// Ẩn radioInputs khi click bên ngoài
document.addEventListener('click', function (e) {
    if (!e.target.closest('.add-to-cart') && !e.target.closest('.radio-inputs')) {
        radioInputs.style.display = 'none';
    }
});

