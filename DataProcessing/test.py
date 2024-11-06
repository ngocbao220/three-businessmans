import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
df = pd.DataFrame(columns=['Xã/Phường', 'Quận/Huyện', 'Chủ đầu tư', 'Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất', 'Thông tin khác', 'Lịch sử giá'])
df.to_csv('Data/data_original.csv', mode='w', index=False, encoding='utf-8-sig')

try:
    # Open the website
    driver.get('https://batdongsan.com.vn')

    # Wait for the login button and click it
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Đăng nhập')]")))
    login_button.click()

    # Wait for the login form to appear and fill in the login details
    wait.until(EC.presence_of_element_located((By.ID, 'username')))  # Change 'username' to the actual ID of the username field
    username_field = driver.find_element(By.ID, 'username')  # Replace with the actual ID for the username field
    password_field = driver.find_element(By.ID, 'password')  # Replace with the actual ID for the password field

    # Input login credentials
    username_field.send_keys('0383616890')  # Replace 'your_username' with your actual username
    password_field.send_keys('Reyn11032005')  # Replace 'your_password' with your actual password

    # Click the login button
    login_submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Đăng nhập')]")
    login_submit_button.click()

    # Wait for login to complete (adjust as needed)
    time.sleep(3)

    # Function to scrape property details
    def get_property_details():
        try:
            area_element = driver.find_element(By.CLASS_NAME, 're__pr-short-description')
            area = area_element.text.strip()

            # Split area into Xã/Phường and Quận/Huyện
            area_parts = area.split(", ")
            if len(area_parts) >= 2:
                xa_phuong = area_parts[-3]  # Xã/Phường is the part before Quận/Huyện
                quan_huyen = area_parts[-2]  # Quận/Huyện is the last part
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

        # Extract room details
        so_phong_ngu = details['Số phòng ngủ']
        so_toilet = details['Số toilet']

        # Extract price history for the past 2 years
        price_history = ""
        try:
            # Find the element containing price history
            history_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Lịch sử giá')]")))
            history_button.click()
            time.sleep(2)  # Wait for history to load

            # Find price data (change the selector based on the actual HTML structure)
            price_elements = driver.find_elements(By.XPATH, "//div[@class='history-price-item']")
            for element in price_elements:
                try:
                    price_month = element.find_element(By.CLASS_NAME, 'history-price-month').text
                    price_value = element.find_element(By.CLASS_NAME, 'history-price-value').text
                    price_history += f"{price_month}: {price_value}, "
                except:
                    continue
        except:
            price_history = "Không có thông tin lịch sử giá"

        # Append all the data into a new row
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
            'Thông tin khác': "; ".join(other_info),
            'Lịch sử giá': price_history
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
