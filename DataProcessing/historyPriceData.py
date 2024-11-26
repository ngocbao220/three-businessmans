import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
import os
import sys
import unicodedata
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Prediction')))
from model import Predictor

# Địa chỉ các file cần thiết
data_path = './Data/cleanedData/cleaned_data.csv'
month_price_path = './Data/priceData/month_price.csv'
quarter_price_path = './Data/priceData/quarter_price.csv'
# Tạo DataFrame 
month_prices = pd.read_csv(month_price_path)
quarter_prices = pd.read_csv(quarter_price_path)
data = pd.read_csv(data_path)

# Các khu vực trên thành phố Hà Nội
# area_names = data['Quận/Huyện'].drop_duplicates().to_list()
area_names = ['Nam Từ Liêm', 'Bắc Từ Liêm', 'Hà Nội']
project_names = data['Tên dự án'].drop_duplicates().to_list()
# Tài nguyên chuyển đổi giá theo Quý sang theo Tháng
columns = 'Giá T10/22,Giá T11/22,Giá T12/22,Giá T1/23,Giá T2/23,Giá T3/23,Giá T4/23,Giá T5/23,Giá T6/23,Giá T7/23,Giá T8/23,Giá T9/23,Giá T10/23,Giá T11/23,Giá T12/23,Giá T1/24,Giá T2/24,Giá T3/24,Giá T4/24,Giá T5/24,Giá T6/24,Giá T7/24,Giá T8/24,Giá T9/24,Giá T10/24'
quarter_to_months = {
    'Giá Q4/22': ['Giá T10/22', 'Giá T11/22', 'Giá T12/22'],
    'Giá Q1/23': ['Giá T1/23', 'Giá T2/23', 'Giá T3/23'],
    'Giá Q2/23': ['Giá T4/23', 'Giá T5/23', 'Giá T6/23'],
    'Giá Q3/23': ['Giá T7/23', 'Giá T8/23', 'Giá T9/23'],
    'Giá Q4/23': ['Giá T10/23', 'Giá T11/23', 'Giá T12/23'],
    'Giá Q1/24': ['Giá T1/24', 'Giá T2/24', 'Giá T3/24'],
    'Giá Q2/24': ['Giá T4/24', 'Giá T5/24', 'Giá T6/24'],
    'Giá Q3/24': ['Giá T7/24', 'Giá T8/24', 'Giá T9/24', 'Giá T10/24']
}

# Hàm chuyển đổi
def change_quarter_to_month(quarter_row):
    result = pd.DataFrame(columns=columns.split(','))
    for quarter, months in quarter_to_months.items():
        if quarter in quarter_row:
            for month in months:
                result[month] = quarter_row[quarter]
    
    return result
# Hàm chuẩn hóa địa chỉ file
def normalize_area_name(area_name):
    # Bỏ dấu tiếng Việt
    area_name = unicodedata.normalize('NFD', area_name)
    area_name = ''.join(ch for ch in area_name if unicodedata.category(ch) != 'Mn')

    # Chuyển tất cả sang chữ thường
    area_name = area_name.lower()

    # Thay dấu cách và các ký tự không hợp lệ bằng dấu gạch dưới
    area_name = re.sub(r'\s+', '_', area_name)  # Thay khoảng trắng

    return area_name

# Tạo class lấy dữ liệu giá của các khu vực
class historyPrice:
    def __init__(self, area = None):
        if area != 'Hà Nội':
            self.data = data[data['Quận/Huyện'] == area]
        elif(area == 'Hà Nội'):
            self.data = data
        self.area_name = area
        self.allPrices = pd.DataFrame(columns=columns.split(',')) # DataFrame chứa toàn bộ dữ liệu giá
        self.mean_price = pd.DataFrame(columns=columns.split(',')) # DataFrame chứa giá trung bình

    # Thêm toàn bộ lịch sử giá vào DataFrame 
    def addToAllPrice(self):
        for index, row in self.data.iterrows():
            if row['Mã lịch sử giá'] == 'M':
                matching_row = month_prices[month_prices['index'] == index].drop(columns=['index'])
                if not matching_row.empty:
                    self.allPrices = pd.concat([self.allPrices, matching_row], ignore_index=True)
            if row['Mã lịch sử giá'] == 'Q':
                matching_row = quarter_prices[quarter_prices['index'] == index].drop(columns=['index'])
                if not matching_row.empty:
                    self.allPrices = pd.concat([self.allPrices, change_quarter_to_month(matching_row)], ignore_index=True)
    
    # Lấy giá trung bình
    def makeMeanPrice(self):
        self.addToAllPrice()
        less = []
        mean = []
        max = []

        for col in self.allPrices.columns:
            less.clear()
            mean.clear()
            max.clear()
            for row in self.allPrices[col]:
                if isinstance(row, str):
                    row_values = row.split()
                    less.append(float(row_values[0]))
                    mean.append(float(row_values[1]))
                    max.append(float(row_values[2]))

            self.mean_price[col] = [round(np.min(less), 2), round(np.mean(mean), 2), round(np.max(max), 2)]
    
    # Thêm phần dự đoán
    def addPredictionData(self):
        predictor_max = Predictor(self.mean_price.columns.str.replace('Giá', ""), self.mean_price.loc[2,:])
        predictor_mean = Predictor(self.mean_price.columns.str.replace('Giá', ""), self.mean_price.loc[1,:])
        predictor_min = Predictor(self.mean_price.columns.str.replace('Giá', ""), self.mean_price.loc[0,:])

        self.mean_price['Giá T11/24'] = [
        round(predictor_min.prediction(), 2),
        round(predictor_mean.prediction(), 2),
        round(predictor_max.prediction(), 2)
        ]
    
    # Ghi dữ liệu giá vào tệp JSON
    def toJson(self, base_json_path):
        if self.area_name is not None:
            self.makeMeanPrice()
            self.addPredictionData()
            json_path = os.path.join(base_json_path, f"{normalize_area_name(self.area_name)}.json")
            self.mean_price.to_json(json_path, orient="records", indent=4, force_ascii=False)
        else:
            for area_name in area_names:
                hP = historyPrice(area_name)
                hP.makeMeanPrice()
                hP.addPredictionData()
                json_path = os.path.join(base_json_path, f"{normalize_area_name(area_name)}.json")
                hP.mean_price.to_json(json_path, orient="records", indent=4, force_ascii=False)

# Thực hiện chạy các hàm để thêm dữ liệu
hP = historyPrice()
hP.toJson('./HighchartsProject/Json/History_Price/area')