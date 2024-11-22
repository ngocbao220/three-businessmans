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

# Chắc chắn là thư mục data tồn tại
if not os.path.exists('Data'):
    os.makedirs('Data')

# Đường dẫn tới file data csv basic và project
page_new_Path = 'Data/page_number_new.txt'
data_new_Path = 'Data/originalData/data_original_new.csv'
data_Project_new_Path = 'Data/originalData/data_project_new.csv'
# Tạo trình điều khiển Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

'''# Tạo 1 dataframe chứa các cột của data
df = pd.DataFrame(columns=['Xã/Phường', 'Quận/Huyện', 'Tỉnh/Thành phố', 'Chủ đầu tư','Tên dự án', 'Phân loại', 'Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất', 'Mặt tiền', 'Hướng nhà', 'Hướng ban công', 'Thông tin khác', 'Lịch sử giá', 'Khoảng giá'])
df.to_csv(data_new_Path, mode='a', index=False, encoding='utf-8-sig')
df.to_csv(data_Project_new_Path, mode='a', index=False, encoding='utf-8-sig')'''

try:
    # URL của trang web bất động sản
    url = 'https://batdongsan.com.vn/nha-dat-ban-ha-noi'
    driver.get(url)
    time.sleep(20) # Sleep để login bằng cơm

    # Chờ load xong trang
    wait = WebDriverWait(driver, 5)

    # Hàm ấnh nút lịch sử giá
    def click_price_history_button():        
        try:
            price_history_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.re__clearfix.clear .re__block-ldp-pricing-cta')))
            price_history_button.click()
            return 1
        except:
            print("Không tìm thấy nút lịch sử giá.")
            return 0
        
    # Hàm lấy lịch sử giá, trả về lịch sử giá và lịch sử khoảng giá
    def get_price_history():
        try:
            # Chờ tới khi biểu đồ lịch sử giá hiển thị
            canvas = wait.until(EC.visibility_of_element_located((By.ID, 'chart-canvas')))
            
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", canvas)
            time.sleep(0.5)  

            canvas_width = canvas.size['width']
            canvas_height = canvas.size['height']

            action = ActionChains(driver)
            price_history = []
            price_spread_history = []
            
            # Tính khoảng cách giữa các điểm
            step = max(0.85, int(canvas_width / 25))  
            
            # Chạy từng điểm trên biểu đồ giá
            for x in range(0, canvas_width - 10, step):  
                try:
                    action.move_to_element_with_offset(canvas, x - 320, canvas_height // 2).perform()
                    time.sleep(0.1)  # Chờ tới khi tooltip hiển thị

                    # Tìm tooltip và lấy dữ liệu lịch sử giá
                    tooltip = driver.find_element(By.ID, 'chartjs-tooltip')
                    period = tooltip.find_element(By.XPATH, ".//span[@class='txt-left color']").text
                    price = tooltip.find_element(By.XPATH, ".//span[@class='txt-right color']").text
                    price_history.append(f"{period} {price}")
                    #print(f"Data at x={x}: {period} - {price}")

                    price_spread = tooltip.find_element(By.XPATH, ".//span[@class='txt-right']").text
                    lowest_price = (price_spread.split()[0])
                    highest_price = (price_spread.split()[2])
                    price_spread_history.append(f"{lowest_price} {highest_price}")
                    #print(f"Data at x={x}: {lowest_price} - {highest_price}")

                except Exception as e:
                    continue  

            return ("; ".join(price_history) if price_history 
                                            else "Không có dữ liệu lịch sử giá",
                    "; ".join(price_spread_history) if  price_spread_history 
                                                    else "Không có dữ liệu lịch sử khoảng giá"
                    )
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu lịch sử giá")
            return ("Không có dữ liệu lịch sử giá",
                    "Không có dữ liệu lịch sử khoảng giá"
                    )
        
    # Hàm lấy thông tin bất động sản
    def get_property_details():
        try:
            price_history = 'Không có dữ liệu lịch sử giá'
            price_spread_history = 'Không có dữ liệu lịch sử khoảng giá'
            investor_name = 'Không có thông tin'
            project_name = 'Không có thông tin'
            classify = 'Không thể phân loại'

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 're__pr-short-description')))

            area_element = driver.find_element(By.CLASS_NAME, 're__pr-short-description')
            area = area_element.text.strip()
            area_parts = area.split(", ")

            commune_ward = area_parts[-3] if len(area_parts) >= 2 else "Không tìm thấy"
            district = area_parts[-2] if len(area_parts) >= 2 else "Không tìm thấy"
            province_city = area_parts[-1] if len(area_parts) >= 2 else "Không tìm thấy"
            
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 're__ldp-project-info')))

                # Lấy thông tin cđt, vì cùng class name với cái khác nên phải dùng css selector
                investor = driver.find_element(By.CSS_SELECTOR, ".re__footer-content .re__long-text")
                investor_name = investor.text if investor else "Không có thông tin"

                # Lấy thông tin dự án
                project = driver.find_element(By.CLASS_NAME, 're__project-title')
                project_name = project.text if project else "Không có thông tin"
            except:
                print("Không có thông tin cđt và dự án bất động sản")
                
            
            details = {'Diện tích': 'Không có thông tin', 
                       'Mức giá': 'Không có thông tin', 
                       'Số phòng ngủ': 'Không có thông tin', 
                       'Số toilet': 'Không có thông tin', 
                       'Pháp lý': 'Không có thông tin', 
                       'Nội thất': 'Không có thông tin', 
                       'Mặt tiền': 'Không có thông tin', 
                       'Hướng nhà': 'Không có thông tin',
                       'Hướng ban công': 'Không có thông tin',
            }

            other_info = []
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 're__pr-specs-content-item')))
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
            
            # Tìm số tòa/căn
            try:
                elements = driver.find_elements(By.CLASS_NAME, "re__prj-card-config-value")
                for element in elements:
                    aria_label = element.get_attribute("aria-label") 

                    if "căn hộ" in aria_label:  # Phần tử chứa thông tin căn hộ
                        num_apartments = element.text
                    elif "tòa nhà" in aria_label:  # Phần tử chứa thông tin tòa nhà
                        num_buildings = element.text

                other_info.append(f"{'Số tòa'}: {num_buildings}")
                other_info.append(f"{'Số căn hộ'}: {num_apartments}")
            except:
                print('Không có thông tin tòa/căn')

            # Phân loại bđt
            try:
                classify = driver.find_element(By.XPATH, '//a[@class="re__link-se" and @level="4"]').text
            except:
                print('Không thể phân loại')

            if(len(other_info) == 0):
                other_info.append("Không có thông tin")

            # Kiểm tra xem có lịch sử giá không
            if (click_price_history_button()):
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 're__tab-box-group')))
                    two_years_tab = driver.find_element(By.XPATH, "//li[@data-val='7bd57ad3dfa6ce4b']")
                    
                    # Cuộn trang đến tab để đảm bảo phần tử này hiển thị trên màn hình
                    driver.execute_script("arguments[0].scrollIntoView(true);", two_years_tab)
                    time.sleep(1)  # Đợi một chút sau khi cuộn

                    # Kiểm tra xem tab đã được chọn chưa, nếu chưa thì click vào
                    if 're__tab-box--active' not in two_years_tab.get_attribute('class'):
                        #print("Tab '2 năm' chưa được chọn, tiến hành click")
                        # Sử dụng JavaScriptExecutor để click nếu thao tác click bình thường không thành công
                        two_years_tab.click()
                        #print("Đã chuyển sang tab '2 năm'")
                    else:
                        print("Tab '2 năm' đã được chọn")
                    time.sleep(1)  # Đợi một chút sau khi nhấp vào tab

                    # Gọi hàm để lấy giá và khoảng giá trong lịch sử
                    get_price_history_data = get_price_history()
                    price_history = get_price_history_data[0]
                    price_spread_history = get_price_history_data[1]

                except Exception as e:
                    print(f"Không thể chuyển sang tab '2 năm'")
                
            new_row = pd.DataFrame([{
                'Xã/Phường': commune_ward,
                'Quận/Huyện': district,
                'Tỉnh/Thành phố': province_city,
                'Chủ đầu tư': investor_name,
                'Tên dự án': project_name,
                'Phân loại': classify,
                'Diện tích': details['Diện tích'],
                'Mức giá': details['Mức giá'],
                'Số phòng ngủ': details['Số phòng ngủ'],
                'Số toilet': details['Số toilet'],
                'Pháp lý': details['Pháp lý'],
                'Nội thất': details['Nội thất'],
                'Mặt tiền': details['Mặt tiền'],
                'Hướng nhà': details['Hướng nhà'],
                'Hướng ban công': details['Hướng ban công'],
                'Thông tin khác': "; ".join(other_info),
                'Lịch sử giá': price_history,
                'Khoảng giá': price_spread_history
            }])

            ''' In từng lịch sử giá từng tháng
            for col in price_history.split("; "):
                print(col) '''

            # Ghi dữ liệu vào file CSV
            if (investor_name != "Không có thông tin"):
                # File CSV dự án và có lịch sử giá
                new_row.to_csv(data_Project_new_Path, mode='a', index=False, header=False, encoding='utf-8-sig')
            # File CSV basic
            new_row.to_csv(data_new_Path, mode='a', index=False, header=False, encoding='utf-8-sig')

        except Exception as e:
            print(f"Lỗi khi lấy thông tin bất động sản")

    # Hàm duyệt trang
    def navigate_pagination():
        number_of_pages = 1
        # 'ba-dinh', 'hoan-kiem', 'tay-ho', 'long-bien', 'cau-giay', 'dong-da', 'hai-ba-trung', 'hoang-mai', 'thanh-xuan', 'ha-dong', 'bac-tu-liem', 'nam-tu-liem', 'son-tay', 'ba-vi', 'chuong-my', 'dan-phuong', 'dong-anh', 'gia-lam', 'hoai-duc', 'me-linh', 'my-duc', 'phu-xuyen', 'phuc-tho', 'quoc-oai', 'soc-son', 'thach-that', 'thanh-oai', 'thanh-tri', 'thuong-tin', 'ung-hoa'
        areas = ['hoan-kiem', 'tay-ho', 'long-bien', 'cau-giay', 'dong-da', 'hai-ba-trung', 'hoang-mai', 'thanh-xuan', 'ha-dong']
        classify_links = ['ban-can-ho-chung-cu-', 'ban-nha-dat-', 'ban-dat-dat-nen-', 'ban-trang-trai-khu-nghi-duong-', 'ban-kho-nha-xuong-', 'ban-loai-bat-dong-san-khac-']
        count_of_data = 0
        for area in areas:
            for classify_link in classify_links:
                count_of_data = 0
                number_of_pages = 1
                url_page =  'https://batdongsan.com.vn/' + classify_link + area + '/p' + str(number_of_pages)
                print(url_page)
                driver.get(url_page)
                while True:
                    property_links = driver.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id')
                    property_urls = [link.get_attribute('href') for link in property_links]

                    for property_url in property_urls:
                        driver.get(property_url)
                        time.sleep(0.5)
                        get_property_details()
                        count_of_data += 1
                    
                    if count_of_data >= 200:
                        break

                    number_of_pages += 1


                    try:
                        url_page =  'https://batdongsan.com.vn/' + classify_link + area + '/p' + str(number_of_pages)
                        with open(page_new_Path, "w", encoding="utf-8") as file:
                            file.write(url_page)
                        driver.get(url_page)
                        time.sleep(0.5)

                        empty_class = driver.find_element(By.CLASS_NAME, "re__srp-empty")
                        check = empty_class.find_element(By.TAG_NAME, "p").text
                        if check == 'Không có kết quả nào phù hợp':
                            break 
                    except:
                        print("Đã duyệt hết tất cả các trang")
                        break

    # Chạy hàm duyệt trang
    navigate_pagination()

finally:
    driver.quit()
