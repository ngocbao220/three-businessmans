import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

# Ensure the data directory exists
if not os.path.exists('Data'):
    os.makedirs('Data')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Create an empty DataFrame with column headers
df = pd.DataFrame(columns=['Khu vực', 'Chủ đầu tư', 'Diện tích', 'Mức giá', 'Số phòng', 'Pháp lý', 'Nội thất', 'Thông tin khác'])

# Write the header only once at the beginning
df.to_csv('Data/data_original.csv', mode='w', index=False, encoding='utf-8-sig')

try:
    # URL of the real estate website
    url = 'https://batdongsan.com.vn/nha-dat-ban-ha-noi'
    driver.get(url)

    # Wait for the page to load
    wait = WebDriverWait(driver, 10)

    # Function to scrape property details

    def get_property_details():
        try:
            area_element = driver.find_element(By.CLASS_NAME, 're__pr-short-description')
            area = area_element.text.strip()
        except:
            area = "Không tìm thấy khu vực"

        try:
            investor = driver.find_element(By.XPATH, "//div[@class='re__row-item re__footer-content']//span[@class='re__long-text']")
            investor_name = investor.text
        except:
            investor_name = "Không có thông tin"

        details = {
            'Diện tích': 'Không có thông tin', 'Mức giá': 'Không có thông tin',
            'Số tầng': 'Không có thông tin', 'Số phòng ngủ': 'Không có thông tin',
            'Số toilet': 'Không có thông tin', 'Pháp lý': 'Không có thông tin',
            'Nội thất': 'Không có thông tin'
        }
        other_info = []

        specs_items = driver.find_elements(By.CLASS_NAME, 're__pr-specs-content-item')
        for item in specs_items:
            try:
                spec_title = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-title').text
                spec_value = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-value').text
                if spec_title in details:
                    details[spec_title] = spec_value
                else:
                    other_info.append(f"{spec_title}: {spec_value}")
            except:
                continue

        room_info = f"Số tầng: {details['Số tầng']}, Số phòng ngủ: {details['Số phòng ngủ']}, Số toilet: {details['Số toilet']}"
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
        new_row.to_csv('Data/data_original.csv', mode='a', index=False, header=False, encoding='utf-8-sig')

        # Hàm để duyệt phân trang
    def navigate_pagination():
        page_number = 1
        current_page_url = driver.current_url  # Lưu URL của trang đầu tiên

        while True:
            # Lấy danh sách các liên kết đến bất động sản từ trang hiện tại
            property_links = driver.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id')
            # Lấy các URL từ các liên kết đã được lọc
            property_urls = [link.get_attribute('href') for link in property_links]

            # Duyệt qua từng liên kết bất động sản
            for property_url in property_urls:
                driver.get(property_url)  # Truy cập vào trang chi tiết của bất động sản
                time.sleep(0.5)  # Đợi trang chi tiết tải
                get_property_details()  # Gọi hàm lấy chi tiết

            driver.get(current_page_url)  # Quay lại URL của trang hiện tại
            time.sleep(0.5)  # Đợi trang hiện tại tải lại

            # Chuyển trang tiếp theo
            try:
                page_number += 1
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@pid='{page_number}']")))
                next_button.click()
                    
                # Cập nhật URL của trang hiện tại sau khi chuyển trang
                current_page_url = driver.current_url
            except:
                print("Đã duyệt hết tất cả các trang")
                break

    # Chạy hàm duyệt phân trang
    navigate_pagination()

finally:
    driver.quit()
