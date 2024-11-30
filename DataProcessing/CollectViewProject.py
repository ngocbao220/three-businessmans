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


data_Project_new_Path = 'D:\\AI - năm hai\\Kì I\LT xử lý dữ liệu\\BTL\\three-businessmans\\Data\\originalData\\data_project_new.csv'
data_Project_view_Path = 'D:\\AI - năm hai\\Kì I\LT xử lý dữ liệu\\BTL\\three-businessmans\\Data\\originalData\\data_project_view.csv'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

df = pd.read_csv(data_Project_new_Path)
project_name_dict = {}

def get_project_data_dict(historyPriceOfProject):
    if pd.isna(historyPriceOfProject) or historyPriceOfProject.strip() == "Không có dữ liệu lịch sử giá":
        return None
    
    # Tách các giá trị theo dấu ;
    gia_list = [re.findall(r"(\d+,\d+) tr/m²", gia.strip()) for gia in historyPriceOfProject.split(";") if "Giá" in gia]
    # Loại bỏ các giá trị rỗng hoặc không hợp lệ
    gia_list = [float(gia[0].replace(",", ".")) for gia in gia_list if gia]
    return gia_list[-1] if gia_list else None

# Tạo cột "Giá cuối" với giá trị cuối cùng
df["Giá trung bình"] = df["Lịch sử giá"].apply(get_project_data_dict)

# Lọc ra DataFrame chỉ chứa các hàng có giá trị "Giá cuối" không null
df_result = df[df["Giá trung bình"].notna()][["Tên dự án", "Giá cuối"]]


def change_name_to_url(ProjectName):
    # Chuyển thành chữ thường
    ProjectName = unidecode(ProjectName.lower())
    # Thay thế ký tự đặc biệt và khoảng trắng bằng dấu gạch ngang
    ProjectName = re.sub(r"[^\w\s]", "", ProjectName)  # Loại bỏ dấu câu
    ProjectName = re.sub(r"\s+", "-", ProjectName)  # Thay thế khoảng trắng bằng gạch ngang
    return ProjectName

df_result['Tên dự án URL'] = df_result['Tên dự án'].apply(change_name_to_url)
df_result.drop_duplicates(inplace=True)

#print(df_result)

list_of_view = []

for url_name in df_result["Tên dự án URL"]:

    url = 'https://batdongsan.com.vn/nha-dat-ban-' + url_name
    driver.get(url)
    try:
        
        element = driver.find_element(By.CLASS_NAME, "re__srp-traffic-label")
        view_text = element.text
        
        view = int("".join(filter(str.isdigit, view_text)))
        list_of_view.append(view)

    except Exception as e:
        print(f"Không tìm thấy thông tin số lượt xem")
        list_of_view.append(0)

df_result['Lượt xem'] = list_of_view

df_result.to_csv(data_Project_view_Path, index=False)
