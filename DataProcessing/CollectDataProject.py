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
wait = WebDriverWait(driver, 20)


def change_name_to_url(ProjectName):
    # Chuyển thành chữ thường
    ProjectName = unidecode(ProjectName.lower())
    # Thay thế ký tự đặc biệt và khoảng trắng bằng dấu gạch ngang
    ProjectName = re.sub(r"[^\w\s]", "", ProjectName)  # Loại bỏ dấu câu
    ProjectName = re.sub(r"\s+", "-", ProjectName)  # Thay thế khoảng trắng bằng gạch ngang
    return ProjectName

df['Tên dự án URL'] = df['Tên dự án'].apply(change_name_to_url)

df = df.drop_duplicates(subset='Tên dự án', keep='first')

print(df.shape[0])
total = 589
count_data = 0
for index, row in df.iterrows():
    if count_data < total:
        count_data = count_data + 1
        continue

    commune_ward = row["Xã/Phường"]
    district = row["Quận/Huyện"]
    province_city = row["Tỉnh/Thành phố"]
    project_name = row["Tên dự án"]
    investor = row["Chủ đầu tư"]
    url_name = row["Tên dự án URL"]
    area = 'Không có thông tin'
    number_of_apartments = 'Không có thông tin'
    number_of_buildings = 'Không có thông tin'
    legal_status = 'Không có thông tin'
    list_of_links = []
    utilities = []
    projectID = 'Không có thông tin'
    history_price = row["Lịch sử giá"]

    url = 'https://batdongsan.com.vn/nha-dat-ban-' + url_name
    driver.get(url)
    time.sleep(1)

    try:
        button = driver.find_element(By.XPATH, '//a[text()="Xem chi tiết dự án"]')
        time.sleep(1)
        # Click vào nút
        ActionChains(driver).move_to_element(button).click().perform()
        time.sleep(1)
    except:
        print('Không ấn được nút:' + url)
        new_row = pd.DataFrame([{
                'Xã/Phường': commune_ward,
                'Quận/Huyện': district,
                'Tỉnh/Thành phố': province_city,
                'Tên dự án': project_name,
                'Chủ đầu tư': investor,
                'Diện tích': area,
                'Số căn hộ': number_of_apartments,
                'Số tòa': number_of_buildings,
                'Pháp lý': legal_status,
                'Link ảnh': 'Không có thông tin',
                'Tiện ích': 'Không có thông tin',
                'Project ID': projectID,
                'Lịch sử giá': history_price,
            }])
        new_row.to_csv(data_Project_only_Path, mode='a', index=False, header=False, encoding='utf-8-sig')
        
        continue


    try:
        tabs = driver.window_handles

        
        driver.switch_to.window(tabs[0])  
        driver.close()  

        # Chuyển sang tab thu hai
        driver.switch_to.window(tabs[1])
        time.sleep(1)
        
    except:
        print('Không chuyển được tab')
        
        continue


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

        list_of_links = video_links + image_links
    except:
        list_of_links.append('Không có hình ảnh')
        print('Không có hình ảnh')
        

    
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".re__toogle-icon.re__icon-chevron-down"))
    )
    
    # Tìm phần tử biểu tượng mũi tên xuống và nhấp vào
    toggle_icon = driver.find_element(By.CSS_SELECTOR, ".re__toogle-icon.re__icon-chevron-down")
    toggle_icon.click()  # Nhấp vào để mở thông tin
    time.sleep(2)
    
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
                
                if label == 'Diện tích':
                    area = value
                    
                elif label == 'Diện tích xây dựng':
                    area = value
                    
                elif label == 'Số tòa':
                    number_of_buildings = value
                    
                elif label == 'Số căn hộ':
                    number_of_apartments = value
                    
                elif label == 'Pháp lý':
                    legal_status = value
            except:
                print('Không có thông tin')
                

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".re__project-toogle.re__prj-facilities .re__toogle-icon.re__icon-chevron-down"))
        )
        
        # Tìm phần tử biểu tượng mũi tên xuống của phần Tiện ích và nhấp vào
        toggle_icon = driver.find_element(By.CSS_SELECTOR, ".re__project-toogle.re__prj-facilities .re__toogle-icon.re__icon-chevron-down")
       
        toggle_icon.click()  # Nhấp vào để mở phần tiện ích
        time.sleep(2)
        # Đợi phần tử thông tin tiện ích xuất hiện
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".js__toogle-detail.re__toogle-detail"))
        )

        # Lấy tất cả các mục tiện ích trong danh sách
        list_items = driver.find_elements(By.CSS_SELECTOR, ".js__toogle-detail.re__toogle-detail ul li")

        
        # Duyệt qua tất cả các phần tử li và lấy thông tin
        for item in list_items:
            # Lấy tên của từng mục
            item_name = item.text.strip()
            utilities.append(item_name)
            #print(item_name)
        
    except:
        utilities.append('Không có thông tin')
        print('Không có thông tin Tiện ích')
        

    try:
        projectID = driver.execute_script("return window.dataLayer.find(item => item.event === 'pageInfo').pro;")
    except:
        projectID = 'Không có thông tin ID'
    #print(projectID)

    new_row = pd.DataFrame([{
                'Xã/Phường': commune_ward,
                'Quận/Huyện': district,
                'Tỉnh/Thành phố': province_city,
                'Tên dự án': project_name,
                'Chủ đầu tư': investor,
                'Diện tích': area,
                'Số căn hộ': number_of_apartments,
                'Số tòa': number_of_buildings,
                'Pháp lý': legal_status,
                'Link ảnh': list_of_links,
                'Tiện ích': utilities,
                'Project ID': projectID,
                'Lịch sử giá': history_price,
            }])
    #print(new_row)
    new_row.to_csv(data_Project_only_Path, mode='a', index=False, header=False, encoding='utf-8-sig')
    