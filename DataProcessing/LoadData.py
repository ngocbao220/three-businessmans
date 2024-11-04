from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Khởi tạo trình duyệt với ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL của trang bất động sản
url = 'https://batdongsan.com.vn/nha-dat-ban-ha-noi'
driver.get(url)

# Đợi trang tải
time.sleep(1)

# Lưu thông tin vào danh sách
property_data = []

# Lấy danh sách các liên kết đến bất động sản từ trang chính
property_links = driver.find_elements(By.CLASS_NAME, 'js__product-link-for-product-id')
property_urls = [link.get_attribute('href') for link in property_links]

# Duyệt qua từng liên kết bất động sản
for property_url in property_urls:
    driver.get(property_url)  # Truy cập vào trang chi tiết của bất động sản
    time.sleep(0.5)  # Đợi trang chi tiết tải

    try:
    # Tìm tất cả các thẻ <a> với class 're__link-se'
        area_elements = driver.find_elements(By.CLASS_NAME, 're__link-se')
    
    # Kiểm tra xem có ít nhất 3 thẻ không
        if len(area_elements) >= 3:
            area = area_elements[2].text.strip()  # Lấy chữ từ thẻ thứ 3
        else:
            area = "Không tìm thấy đủ khu vực"
    except Exception as e:
        area = "Không tìm thấy khu vực"
    
    print(f"Khu vực: {area}")

    # Lấy các phần tử có chứa thông tin đặc trưng
    specs_items = driver.find_elements(By.CLASS_NAME, 're__pr-specs-content-item')

    for item in specs_items:
        try:
            spec_title = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-title').text
            spec_value = item.find_element(By.CLASS_NAME, 're__pr-specs-content-item-value').text
            print(f"{spec_title}: {spec_value}")
        except:
            continue  # Bỏ qua nếu không tìm thấy tiêu đề hoặc giá trị

    # Quay lại trang chính để lấy liên kết tiếp theo
    print("-------------------------------------------")
    driver.get(url)
    time.sleep(0.5)

driver.quit()