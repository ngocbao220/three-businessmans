import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import json

# Chắc chắn là thư mục data tồn tại
if not os.path.exists('Data'):
    os.makedirs('Data')

# Đường dẫn tới file
page_Path = 'Data/page_number.txt'
data_new_Path = 'Data/originalData/data_project_only.csv'

test_Path = 'Data/originalData/test.csv'

# Tạo trình điều khiển Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

'''# Tạo 1 dataframe chứa các cột của data
df = pd.DataFrame(columns=['Xã/Phường', 'Quận/Huyện', 'Tỉnh/Thành phố', 'Tên dự án', 'Giá', 'Diện tích', 'Chủ đầu tư', 'Quy mô', 'Số căn hộ', 'Số tòa', 'Pháp lý', 'Mật độ xây dựng'])
df.to_csv(data_new_Path, mode='a', index=False, encoding='utf-8-sig')
'''
try:
    # URL của trang web bất động sản
    url = 'https://batdongsan.com.vn/du-an-bat-dong-san-ha-noi'
    driver.get(url)
    time.sleep(2) # Sleep để login bằng cơm

    # Chờ load xong trang
    wait = WebDriverWait(driver, 5)
        
    # Hàm lấy thông tin bất động sản
    def get_property_details():
        try:            
        
            try:
                project_name = driver.find_element(By.CSS_SELECTOR, ".re__project-name").text.strip()
            except:
                project_name = "Không tìm thấy tên dự án"
                print(f"Lỗi khi lấy tên dự án: {e}")
            print(project_name)
            try:
                project_address = driver.find_element(By.CSS_SELECTOR, ".re__project-address").text.strip()
                # Loại bỏ phần "Xem bản đồ" 
                if "Xem bản đồ" in project_address:
                    project_address = project_address.replace("Xem bản đồ", "").strip()
            except:
                project_address = "Không tìm thấy địa chỉ"
                print(f"Lỗi khi lấy địa chỉ: {e}")
            print(project_address)

            # Tạo dict để lưu thông tin
            project_info = {
                "Giá": "Không có thông tin",
                "Diện tích": "Không có thông tin",
                "Chủ đầu tư": "Không có thông tin",
                "Quy mô": "Không có thông tin",
                "Số căn hộ": "Không có thông tin",
                "Số tòa": "Không có thông tin",
                "Pháp lý": "Không có thông tin",
                "Mật độ xây dựng": "Không có thông tin",
            }

            elements = driver.find_elements(By.CLASS_NAME, "re__project-box-item")
            print(len(elements))
            # Khởi tạo dictionary để lưu dữ liệu
            for element in elements:
                label = element.find_element(By.TAG_NAME, "label").text  # Lấy nội dung của <label>
                value = element.find_element(By.TAG_NAME, "span").text # Lấy nội dung của <span>

                if label in project_info:
                    project_info[label] = value

            new_row = pd.DataFrame([{
                'Xã/Phường': project_address[-3],
                'Quận/Huyện': project_address[-2],
                'Tỉnh/Thành phố': project_address[-1],
                'Tên dự án': project_name,
            }])
            new_row =pd.DataFrame([project_info])

            # File CSV basic
            #new_row.to_csv(data_new_Path, mode='a', index=False, header=False, encoding='utf-8-sig')

        except Exception as e:
            print(f"Lỗi khi lấy thông tin bất động sản")

    # Hàm duyệt trang
    def navigate_pagination():
        with open(page_Path, "r") as file:
            number_of_pages = int(file.read())
        

        # url_page =  'https://batdongsan.com.vn/du-an-bat-dong-san-ha-noi' + '/p' + str(number_of_pages)

        driver.get(url_page)

        while True:
            property_links = driver.find_elements(By.CSS_SELECTOR, ".js__project-card a")  # Dùng CSS_SELECTOR

            # Trích xuất các URL từ href
            property_urls = [link.get_attribute('href') for link in property_links if link.get_attribute('href')]

            for property_url in property_urls:
                driver.get(property_url)
                time.sleep(0.5)

                get_property_details()

            number_of_pages += 1
            with open(page_Path, "w") as file:
                file.write(str(number_of_pages))
            try:
                url_page =  'https://batdongsan.com.vn/du-an-bat-dong-san-ha-noi' + '/p' + str(number_of_pages)
                
                driver.get(url_page)
                time.sleep(0.5)
                empty_class_1 = driver.find_element(By.CLASS_NAME, "re__srp-empty")
                check_1 = empty_class_1.find_element(By.TAG_NAME, "p").text
                if check_1 == 'Không có kết quả nào phù hợp':
                    print("Đã duyệt hết tất cả các trang 1")
                    break 
            except:
                print("Đã duyệt hết trang")
                continue

    # Chạy hàm duyệt trang
    navigate_pagination()

finally:
    driver.quit()
