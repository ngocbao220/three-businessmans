import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Ensure the data directory exists
if not os.path.exists('Data'):
    os.makedirs('Data')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Create an empty DataFrame with column headers
df = pd.DataFrame(columns=['Xã/Phường', 'Quận/Huyện', 'Chủ đầu tư', 'Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất', 'Thông tin khác'])
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
            
            # Tách thông tin xã/phường và quận/huyện từ chuỗi area
            area_parts = area.split(", ")
            if len(area_parts) >= 2:
                xa_phuong = area_parts[-3]  # Xã/Phường là phần trước quận/huyện
                quan_huyen = area_parts[-2]  # Quận/Huyện là phần cuối
            else:
                xa_phuong, quan_huyen = "Không tìm thấy", "Không tìm thấy"
        except:
            xa_phuong, quan_huyen = "Không tìm thấy", "Không tìm thấy"

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

        # Tách riêng số phòng ngủ và số toilet
        so_phong_ngu = details['Số phòng ngủ']
        so_toilet = details['Số toilet']

        new_row = pd.DataFrame([{
            'Xã/Phường': xa_phuong,
            'Quận/Huyện': quan_huyen,
            'Chủ đầu tư': investor_name,
            'Diện tích': details['Diện tích'],
            'Mức giá': details['Mức giá'],
            'Số phòng ngủ': so_phong_ngu,
            'Số toilet': so_toilet,
            'Pháp lý': details['Pháp lý'],
            'Nội thất': details['Nội thất'],
            'Thông tin khác': "; ".join(other_info)
        }])

        # Append data to the CSV file
        new_row.to_csv('Data/data_original.csv', mode='a', index=False, header=False, encoding='utf-8-sig')

    # Function to navigate pagination
    def navigate_pagination():
        page_number = 1
        current_page_url = driver.current_url  # Save the URL of the current page

        while True:
            # Retrieve the list of property links on the current page
            property_links = driver.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id')
            property_urls = [link.get_attribute('href') for link in property_links]

            # Visit each property link
            for property_url in property_urls:
                driver.get(property_url)
                time.sleep(0.5)
                get_property_details()
                driver.back()
                time.sleep(0.5)

            driver.get(current_page_url)
            time.sleep(0.5)

            # Move to the next page
            try:
                page_number += 1
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@pid='{page_number}']")))
                next_button.click()
                current_page_url = driver.current_url
            except:
                print("Đã duyệt hết tất cả các trang")
                break

    # Run the pagination navigation
    navigate_pagination()

finally:
    driver.quit()
