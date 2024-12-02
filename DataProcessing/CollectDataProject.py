import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from unidecode import unidecode


data_Project_new_Path = 'Data\\originalData\\data_project_new.csv'
data_Project_only_Path = 'Data\\originalData\\data_project_only.csv'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

df = pd.read_csv(data_Project_new_Path)
wait = WebDriverWait(driver, 10)

# Lọc ra DataFrame chỉ chứa các hàng có giá trị "Giá cuối" không null
df_result = df[["Xã/Phường", "Quận/Huyện", "Tên dự án", "Chủ đầu tư"]]
df_result.drop_duplicates(inplace = True)

def change_name_to_url(ProjectName):
    # Chuyển thành chữ thường
    ProjectName = unidecode(ProjectName.lower())
    # Thay thế ký tự đặc biệt và khoảng trắng bằng dấu gạch ngang
    ProjectName = re.sub(r"[^\w\s]", "", ProjectName)  # Loại bỏ dấu câu
    ProjectName = re.sub(r"\s+", "-", ProjectName)  # Thay thế khoảng trắng bằng gạch ngang
    return ProjectName

df_result['Tên dự án URL'] = df_result['Tên dự án'].apply(change_name_to_url)
df_result.drop_duplicates(inplace = True)

df_result = df_result.drop(df_result[df_result['Tên dự án URL'] == 'chung-cu-1517-ngoc-khanh'].index)

df_result = df_result.drop(df_result[df_result['Chủ đầu tư'] == 'Đang cập nhật'].index)

#print(df_result)

area = []
number_of_buildings = []
number_of_apartments = []
legal_status = []
list_of_projectID = []
list_of_links = []
utilities_list = []
for url_name in df_result["Tên dự án URL"]:

    url = 'https://batdongsan.com.vn/nha-dat-ban-' + url_name
    driver.get(url)

    try:
        button = driver.find_element(By.XPATH, '//a[text()="Xem chi tiết dự án"]')
        time.sleep(0.5)
        # Click vào nút
        ActionChains(driver).move_to_element(button).click().perform()
        time.sleep(1)
    except:
        print('Không ấn được nút:' + url)


    try:
        tabs = driver.window_handles

        
        driver.switch_to.window(tabs[0])  
        driver.close()  

        # Chuyển sang tab thu hai
        driver.switch_to.window(tabs[1])
        time.sleep(1)
        
    except:
        print('Không chuyển được tab')


    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".re__project-album__media"))
        )
        media_elements = driver.find_elements(By.CSS_SELECTOR, '.re__project-album__media')

        # Lọc các phần tử video và ảnh
        image_links = []
        video_links = []

        for element in media_elements:
            # Lấy link ảnh
            image_tag = element.find_element(By.TAG_NAME, 'img')
            if image_tag:
                img_src = image_tag.get_attribute('src')
                image_links.append(img_src)
                #print(img_src)
            
            # Lấy link video
            video_tag = element.get_attribute('href')
            if video_tag:
                video_links.append(video_tag)
                #print(video_tag)

        list_of_link = video_links + image_links
        
        list_of_links.append(list_of_link)
    except:
        list_of_links.append('Không có hình ảnh')
        print('Không có hình ảnh')
        continue

    
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".re__toogle-icon.re__icon-chevron-down"))
    )
    
    # Tìm phần tử biểu tượng mũi tên xuống và nhấp vào
    toggle_icon = driver.find_element(By.CSS_SELECTOR, ".re__toogle-icon.re__icon-chevron-down")
    toggle_icon.click()  # Nhấp vào để mở thông tin
    
    # Đợi phần tử thông tin chi tiết xuất hiện
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".re__project-box-wrap"))
    )
    
    # Lấy tất cả các phần tử `.re__project-box-wrap`
    box_wrap_divs = driver.find_elements(By.CSS_SELECTOR, ".re__project-box-wrap")
    
    # Duyệt qua tất cả các phần tử `.re__project-box-wrap`
    for wrap_div in box_wrap_divs:
        # Tìm tất cả các phần tử `.re__project-box-item` bên trong mỗi `.re__project-box-wrap`
        items = wrap_div.find_elements(By.CSS_SELECTOR, ".re__project-box-item")
        
        # Duyệt qua các phần tử `.re__project-box-item` và lấy thông tin
        for item in items:
            try:
                label = item.find_element(By.CSS_SELECTOR, "label").text.strip()  # Lấy tên thông tin
                value = item.find_element(By.CSS_SELECTOR, "span").text.strip()   
                #print(label, value)
                d1 = d2 = d3 = d4 = 0
                if label == 'Diện tích':
                    area.append(value)
                    d1 = 1
                elif label == 'Diện tích xây dựng':
                    area.append(value)
                    d1 = 1
                elif label == 'Số tòa':
                    number_of_buildings.append(value)
                    d2 = 1
                elif label == 'Số căn hộ':
                    number_of_apartments.append(value)
                    d3 = 1
                elif label == 'Pháp lý':
                    legal_status.append(value)
                    d4 = 1

                if d1 == 0:
                    area.append('Không có thông tin')
                if d2 == 0:
                    number_of_buildings.append('Không có thông tin')
                if d3 == 0:
                    number_of_apartments.append('Không có thông tin')
                if d4 == 0:
                    legal_status.append('Không có thông tin')
            except:
                print('Không có thông tin')
                continue

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".re__project-toogle.re__prj-facilities .re__toogle-icon.re__icon-chevron-down"))
        )
        
        # Tìm phần tử biểu tượng mũi tên xuống của phần Tiện ích và nhấp vào
        toggle_icon = driver.find_element(By.CSS_SELECTOR, ".re__project-toogle.re__prj-facilities .re__toogle-icon.re__icon-chevron-down")
        toggle_icon.click()  # Nhấp vào để mở phần tiện ích

        # Đợi phần tử thông tin tiện ích xuất hiện
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js__toogle-detail.re__toogle-detail"))
        )

        # Lấy tất cả các mục tiện ích trong danh sách
        list_items = driver.find_elements(By.CSS_SELECTOR, ".js__toogle-detail.re__toogle-detail ul li")

        utilities = []
        # Duyệt qua tất cả các phần tử li và lấy thông tin
        for item in list_items:
            # Lấy tên của từng mục
            item_name = item.text.strip()
            utilities.append(item_name)
            #print(item_name)
        utilities_list.append(utilities)
    except:
        utilities_list.append('Không có thông tin')
        print('Không có thông tin Tiện ích')
        continue

    try:
        projectID = driver.execute_script("return window.dataLayer.find(item => item.event === 'pageInfo').pro;")

        list_of_projectID.append(projectID)
    except:
        list_of_projectID.append('Không có thông tin ID')
    #print(projectID)


df_result['Diện tích'] = area
df_result['Số tòa'] = number_of_buildings
df_result['Số căn hộ'] = number_of_apartments
df_result['Pháp lý'] = legal_status
df_result['Link ảnh'] = list_of_links
df_result['Tiện ích'] = utilities_list
df_result['Project ID'] = list_of_projectID
df_result['Lịch sử giá'] = df["Lịch sử giá"]

df_result.to_csv(data_Project_only_Path, mode='a', index=False, encoding='utf-8-sig')
