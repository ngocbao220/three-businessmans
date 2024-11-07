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

# Ensure the data directory exists
if not os.path.exists('Data'):
    os.makedirs('Data')

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Create an empty DataFrame with column headers
df = pd.DataFrame(columns=['Xã/Phường', 'Quận/Huyện', 'Chủ đầu tư', 'Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất', 'Mặt tiền', 'Hướng nhà', 'Thông tin khác', 'Lịch sử giá'])
df.to_csv('Data/data_original.csv', mode='w', index=False, encoding='utf-8-sig')

try:
    # URL of the real estate website
    url = 'https://batdongsan.com.vn/nha-dat-ban-ha-noi'
    driver.get(url)
    time.sleep(20)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)

    # Function to scrape price history details
    def click_price_history_button():
        try:
            # Use a specific selector to target the inner div with class `re__block-ldp-pricing-cta`
            price_history_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.re__clearfix.clear .re__block-ldp-pricing-cta')))
            
            # Scroll to the button and click using JavaScript
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", price_history_button)
            time.sleep(1)  # Wait for scroll to complete
            driver.execute_script("arguments[0].click();", price_history_button)  # Click using JavaScript
            print("Successfully clicked on the price history button.")
            
        except Exception as e:
            print(f"Could not click on the price history button: {e}")

    def get_price_history():
        try:
            # Wait until the canvas (price history chart) is visible
            canvas = wait.until(EC.visibility_of_element_located((By.ID, 'chart-canvas')))
            
            # Scroll the canvas element into view
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", canvas)
            time.sleep(1)  # Wait a bit after scrolling to ensure it's in view

            # Get canvas dimensions
            canvas_width = canvas.size['width']
            canvas_height = canvas.size['height']

            # Action chain for mouse movements
            action = ActionChains(driver)
            price_history = []
            
            # Calculate step size based on canvas width
            step = max(0.85, int(canvas_width / 25))  # Approximate 25 points across two years
            
            # Iterate over the canvas with safe bounds
            for x in range(0, canvas_width - 10, step):  # Start 10px in from each edge
                try:
                    # Move to position on canvas and wait for tooltip to appear
                    action.move_to_element_with_offset(canvas, x - 320, canvas_height // 2).perform()
                    time.sleep(0.1)  # Wait for tooltip to appear

                    # Locate tooltip and extract data
                    tooltip = driver.find_element(By.ID, 'chartjs-tooltip')
                    period = tooltip.find_element(By.XPATH, ".//span[@class='txt-left color']").text
                    price = tooltip.find_element(By.XPATH, ".//span[@class='txt-right color']").text
                    price_history.append(f"{period}: {price}")
                    print(f"Data at x={x}: {period} - {price}")

                except Exception as e:
                    print(f"Tooltip not found at position {x}: {e}")
                    continue  # Ignore if tooltip is not available

            return "; ".join(price_history) if price_history else "Không có dữ liệu lịch sử giá"
        
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu lịch sử giá: {e}")
            return "Không có dữ liệu lịch sử giá"


    # Function to scrape property details
    def get_property_details():
        try:
            click_price_history_button()
            # Ensure '2 năm' tab is selected
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 're__tab-box-group')))
                two_years_tab = driver.find_element(By.XPATH, "//li[@data-val='7bd57ad3dfa6ce4b']")
                
                # Cuộn trang đến tab để đảm bảo phần tử này hiển thị trên màn hình
                driver.execute_script("arguments[0].scrollIntoView(true);", two_years_tab)
                time.sleep(1)  # Đợi một chút sau khi cuộn

                # Kiểm tra xem tab đã được chọn chưa, nếu chưa thì click vào
                if 're__tab-box--active' not in two_years_tab.get_attribute('class'):
                    print("Tab '2 năm' chưa được chọn, tiến hành click")
                    # Sử dụng JavaScriptExecutor để click nếu thao tác click bình thường không thành công
                    driver.execute_script("arguments[0].click();", two_years_tab)
                    print("Đã chuyển sang tab '2 năm'")
                else:
                    print("Tab '2 năm' đã được chọn")
                time.sleep(1)  # Đợi một chút sau khi nhấp vào tab

            except Exception as e:
                print(f"Không thể chuyển sang tab '2 năm': {e}")

            # Tiếp tục lấy thông tin từ trang bất động sản
            area_element = driver.find_element(By.CLASS_NAME, 're__pr-short-description')
            area = area_element.text.strip()
            area_parts = area.split(", ")
            xa_phuong = area_parts[-3] if len(area_parts) >= 2 else "Không tìm thấy"
            quan_huyen = area_parts[-2] if len(area_parts) >= 2 else "Không tìm thấy"
            
            investor = driver.find_element(By.XPATH, "//div[@class='re__row-item re__footer-content']//span[@class='re__long-text']")
            investor_name = investor.text if investor else "Không có thông tin"

            details = { 'Diện tích': 'Không có thông tin', 'Mức giá': 'Không có thông tin', 'Số phòng ngủ': 'Không có thông tin', 'Số toilet': 'Không có thông tin', 'Pháp lý': 'Không có thông tin', 'Nội thất': 'Không có thông tin' }
            other_info = []
            specs_items = driver.find_elements(By.CLASS_NAME, 're__pr-specs-content-item')
            mat_tien = "Không có thông tin"
            huong_nha = "Không có thông tin"
            
            for item in specs_items:
                try:
                    spec_title = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-title').text
                    spec_value = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-value').text
                    if spec_title == "Mặt tiền":
                        mat_tien = spec_value
                    elif spec_title == "Hướng nhà":
                        huong_nha = spec_value
                    elif spec_title in details:
                        details[spec_title] = spec_value
                    else:
                        other_info.append(f"{spec_title}: {spec_value}")
                except:
                    continue

            # Call function to get price history
            price_history = get_price_history()

            new_row = pd.DataFrame([{
                'Xã/Phường': xa_phuong,
                'Quận/Huyện': quan_huyen,
                'Chủ đầu tư': investor_name,
                'Diện tích': details['Diện tích'],
                'Mức giá': details['Mức giá'],
                'Số phòng ngủ': details['Số phòng ngủ'],
                'Số toilet': details['Số toilet'],
                'Pháp lý': details['Pháp lý'],
                'Nội thất': details['Nội thất'],
                'Mặt tiền': mat_tien,
                'Hướng nhà': huong_nha,
                'Thông tin khác': "; ".join(other_info),
                'Lịch sử giá': price_history
            }])

            # Append data to the CSV file
            new_row.to_csv('Data/data_original.csv', mode='a', index=False, header=False, encoding='utf-8-sig')

        except Exception as e:
            print(f"Lỗi khi lấy thông tin bất động sản: {e}")

    # Function to navigate pagination
    def navigate_pagination():
        page_number = 1
        current_page_url = driver.current_url

        while True:
            property_links = driver.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id')
            property_urls = [link.get_attribute('href') for link in property_links]

            for property_url in property_urls:
                driver.get(property_url)
                time.sleep(0.5)
                get_property_details()
                driver.back()
                time.sleep(0.5)

            driver.get(current_page_url)
            time.sleep(0.5)

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
