from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Khởi tạo trình duyệt với ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # URL của trang bất động sản
    url = 'https://batdongsan.com.vn/nha-dat-ban-ha-noi'
    driver.get(url)

    # Đợi trang tải
    wait = WebDriverWait(driver, 10)

    # Hàm để lấy thông tin bất động sản từ trang chi tiết
    def get_property_details():
        # KHU VỰC
        try:
            area_elements = driver.find_elements(By.CLASS_NAME, 're__link-se')
            if len(area_elements) >= 3:
                area = area_elements[2].text.strip()  # Lấy chữ từ thẻ thứ 3
            else:
                area = "Không tìm thấy đủ khu vực"
        except Exception as e:
            area = "Không tìm thấy khu vực"
        print("Khu vực: ", area)

        # CHỦ ĐẦU TƯ
        try:
            investor = driver.find_element(By.XPATH, "//div[@class='re__row-item re__footer-content']//span[@class='re__long-text']")
            investor_name = investor.text
        except:
            investor_name = "Không có thông tin"
        print("Chủ đầu tư: ", investor_name)

        # THÔNG TIN ĐẶC ĐIỂM
        specs_items = driver.find_elements(By.CLASS_NAME, 're__pr-specs-content-item')
        for item in specs_items:
            try:
                spec_title = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-title').text
                spec_value = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-value').text
                print(f"{spec_title}: {spec_value}")
            except:
                continue  # Bỏ qua nếu không tìm thấy tiêu đề hoặc giá trị

    # Hàm để duyệt phân trang
    def navigate_pagination():
        page_number = 1
        item_count = 0
        while True:
            # Lấy danh sách các liên kết đến bất động sản từ trang chính
            property_links = driver.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id')
            property_urls = [link.get_attribute('href') for link in property_links]

            # Duyệt qua từng liên kết bất động sản
            for property_url in property_urls:
                driver.get(property_url)  # Truy cập vào trang chi tiết của bất động sản
                time.sleep(0.5)  # Đợi trang chi tiết tải
                get_property_details()  # Gọi hàm lấy chi tiết
                print("-------------------------------------------")
                driver.back()  # Quay lại trang chính
                time.sleep(1)  # Đợi trang chính tải lại
                item_count += 1  # Đếm số lần chạy

                # Khi đạt đến 2 lần, nhấp vào nút phân trang
                if item_count == 31:
                    break  # Thoát vòng lặp và chuyển trang

            # Kiểm tra nếu có nút "Trang tiếp theo" hoặc xác định số trang kế tiếp bằng pid
            try:
                page_number += 1
                try:
                    # Cố gắng nhấn nút "Trang tiếp theo" nếu có
                    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 're__pagination-icon') and @pid]")))
                    next_button.click()
                except:
                    # Nếu không có nút "Trang tiếp theo", dùng số trang `pid`
                    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@pid='{page_number}']")))
                    next_button.click()
                    
                item_count = 0  # Đặt lại bộ đếm
                time.sleep(1)  # Đợi trang tải lại
            except:
                print("Đã duyệt hết tất cả các trang hoặc không tìm thấy nút phân trang tiếp theo.")
                break

    # Chạy hàm duyệt phân trang
    navigate_pagination()

finally:
    # Đóng trình duyệt
    driver.quit()
