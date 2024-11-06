import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Khởi tạo trình duyệt với ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Tạo một DataFrame rỗng với các cột tiêu đề
df = pd.DataFrame(columns=['Khu vực', 'Chủ đầu tư', 'Diện tích', 'Mức giá', 'Số phòng', 'Pháp lý', 'Nội thất', 'Thông tin khác'])

try:
    # URL của trang bất động sản
    url = 'https://batdongsan.com.vn/nha-dat-ban-ha-noi'
    driver.get(url)

    # Đợi trang tải
    wait = WebDriverWait(driver, 10)

    # Hàm để lấy thông tin bất động sản từ trang chi tiết
    # Hàm để lấy thông tin bất động sản từ trang chi tiết
    def get_property_details():
        try:
            # KHU VỰC
            area_elements = driver.find_elements(By.CLASS_NAME, 're__link-se')
            area = area_elements[2].text.strip() if len(area_elements) >= 3 else "Không tìm thấy đủ khu vực"
        except Exception as e:
            area = "Không tìm thấy khu vực"

        try:
            # CHỦ ĐẦU TƯ
            investor = driver.find_element(By.XPATH, "//div[@class='re__row-item re__footer-content']//span[@class='re__long-text']")
            investor_name = investor.text
        except:
            investor_name = "Không có thông tin"

        # Các thông tin chi tiết
        details = {'Diện tích': 'Không có thông tin', 'Mức giá': 'Không có thông tin',
                'Số tầng': 'Không có thông tin', 'Số phòng ngủ': 'Không có thông tin',
                'Số toilet': 'Không có thông tin', 'Pháp lý': 'Không có thông tin',
                'Nội thất': 'Không có thông tin'}
        other_info = []

        # Thu thập thông tin đặc điểm
        specs_items = driver.find_elements(By.CLASS_NAME, 're__pr-specs-content-item')
        for item in specs_items:
            try:
                spec_title = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-title').text
                spec_value = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-value').text

                # Kiểm tra và lưu thông tin vào các mục phù hợp
                if spec_title in details:
                    details[spec_title] = spec_value
                else:
                    other_info.append(f"{spec_title}: {spec_value}")
            except:
                continue

        # Tạo chuỗi gộp "Số phòng"
        room_info = f"Số tầng: {details['Số tầng']}, Số phòng ngủ: {details['Số phòng ngủ']}, Số toilet: {details['Số toilet']}"

        # Thêm dữ liệu vào DataFrame tạm thời và ghi vào CSV ngay lập tức
        new_row = pd.DataFrame([{
            'Khu vực': area,
            'Chủ đầu tư': investor_name,
            'Diện tích': details['Diện tích'],
            'Mức giá': details['Mức giá'],
            'Số phòng': room_info,
            'Pháp lý': details['Pháp lý'],
            'Nội thất': details['Nội thất'],
            'Thông tin khác': "; ".join(other_info)
        }])

        # Ghi vào file CSV ngay lập tức
        new_row.to_csv('Data/data_ogirinal.csv', mode='a', index=False, header=False, encoding='utf-8-sig')

    # Hàm để duyệt phân trang
    def navigate_pagination():
        page_number = 1
        while True:
            # Lấy danh sách các liên kết đến bất động sản từ trang chính
            property_links = driver.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id')
            property_urls = [link.get_attribute('href') for link in property_links]

            # Duyệt qua từng liên kết bất động sản
            for property_url in property_urls:
                driver.get(property_url)  # Truy cập vào trang chi tiết của bất động sản
                time.sleep(0.5)  # Đợi trang chi tiết tải
                get_property_details()  # Gọi hàm lấy chi tiết
                driver.back()  # Quay lại trang chính
                time.sleep(1)  # Đợi trang chính tải lại

            # Kiểm tra nếu có nút "Trang tiếp theo"
            try:
                page_number += 1
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 're__pagination-icon') and @pid]")))
                next_button.click()
                time.sleep(1)  # Đợi trang tải lại
            except:
                print("Đã duyệt hết tất cả các trang hoặc không tìm thấy nút phân trang tiếp theo.")
                break

    # Chạy hàm duyệt phân trang
    navigate_pagination()

finally:
    # Đóng trình duyệt
    driver.quit()

# Ghi dữ liệu vào file CSV
df.to_csv('data_ogirinal.csv', index=False, encoding='utf-8-sig')
