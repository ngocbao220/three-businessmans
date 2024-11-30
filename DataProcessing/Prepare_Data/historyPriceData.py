import pandas as pd
import json
import numpy as np
import os
import sys
import unicodedata
import re
# Thêm mã dự đoán
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', 'Prediction')))
from model import Predictor

# Địa chỉ các file cần thiết
data_path = './Data/cleanedData/cleaned_data_new.csv'
month_price_path = './Data/priceData/month_price.csv'
quarter_price_path = './Data/priceData/quarter_price.csv'

# Tạo DataFrame 
month_prices = pd.read_csv(month_price_path)
quarter_prices = pd.read_csv(quarter_price_path)

data = pd.read_csv(data_path)

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
def normalize_name(area_name):
    # Bỏ dấu tiếng Việt
    area_name = unicodedata.normalize('NFD', area_name)
    area_name = ''.join(ch for ch in area_name if unicodedata.category(ch) != 'Mn')
    
    area_name = area_name.replace('đ', 'd')
    area_name = area_name.replace('Đ', 'd')
    area_name = area_name.replace('_', ' ')
    area_name = area_name.replace('-', ' ')
    # Chuyển tất cả sang chữ thường
    area_name = area_name.lower()

    # Thay dấu cách và các ký tự không hợp lệ bằng dấu gạch dưới
    area_name = re.sub(r'\s+', '_', area_name)  # Thay khoảng trắng

    return area_name

# Tạo class lấy dữ liệu giá của các khu vực và dự án

# KHU VỰC
class historyPriceOfArea:
    def __init__(self, area):
        if area != 'Hà Nội':
            self.data = data.loc[data['Quận/Huyện'] == area]
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
            if (less != []) :
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
    def toJson(self):
        self.makeMeanPrice()
        self.addPredictionData()
        json_path = os.path.join(f"./Data/Json/History_Price/area/{normalize_name(self.area_name)}.json")
        self.mean_price.to_json(json_path, orient="records", indent=4, force_ascii=False)

# DỰ ÁN
class historyPriceOfProject:
    def __init__(self, project):
        if project != 'Hà Nội':
            self.data = data.loc[data['Tên dự án'] == project]
        elif(project == 'Hà Nội'):
            self.data = data
        self.project_name = project
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
            if (less != []) :
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
    def toJson(self):
        self.makeMeanPrice()
        self.addPredictionData()
        json_path = os.path.join(f"./Data/Json/History_Price/project/{normalize_name(self.project_name)}.json")
        self.mean_price.to_json(json_path, orient="records", indent=4, force_ascii=False)

# LOẠI HÌNH
class historyPriceOfType:
    def __init__(self, type_name):
        self.data = data.loc[data['Loại hình'] == type_name]
        self.type_name = type_name
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
            if (less != []) :
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
    def toJson(self):
        self.makeMeanPrice()
        self.addPredictionData()
        json_path = os.path.join(f"./Data/Json/History_Price/type/{normalize_name(self.type_name)}.json")
        self.mean_price.to_json(json_path, orient="records", indent=4, force_ascii=False)

# PHÂN KHÚC
class historyPriceOfSegment:
    def __init__(self, type_segment):
       self.type_segment = type_segment
       if type_segment == 'under_50':
           self.data = data[data['Mức giá'] < 50]
       elif type_segment == 'between_50_100':
           self.data = data[(data['Mức giá'] >= 50) & (data['Mức giá'] < 100)]
       elif type_segment == 'between_100_150':
           self.data = data[(data['Mức giá'] >= 100) & (data['Mức giá'] < 150)]
       elif type_segment == 'between_150_200':
           self.data = data[(data['Mức giá'] >= 150) & (data['Mức giá'] < 200)]
       elif type_segment == 'over_200':
           self.data = data[(data['Mức giá'] >= 200)]
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
            if (less != []) :
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
    def toJson(self):
        self.makeMeanPrice()
        self.addPredictionData()
        json_path = os.path.join(f"./Data/Json/History_Price/segment/{normalize_name(self.type_segment)}.json")
        self.mean_price.to_json(json_path, orient="records", indent=4, force_ascii=False)

# Thực hiện chạy các hàm để thêm dữ liệu vào file Json
# ĐÔng anh Phú Xuyên Phúc Thọ Quốc Oai Sóc Sơn Thanh Oai Ứng Hòa Ba Vì Sơn Tây
districts_hanoi = [
    'Hà Nội',"Ba Đình", "Hoàn Kiếm", "Hai Bà Trưng", "Đống Đa", "Tây Hồ", "Cầu Giấy",
    "Thanh Xuân", "Hoàng Mai", "Long Biên", "Hà Đông", "Bắc Từ Liêm", "Nam Từ Liêm",
    "Đan Phượng", "Đông Anh", "Gia Lâm", "Hoài Đức", "Mê Linh", "Mỹ Đức",
    "Phú Xuyên", "Phúc Thọ", "Quốc Oai", "Sóc Sơn", "Thạch Thất", "Thanh Oai",
    "Thanh Trì", "Thường Tín", "Ứng Hòa", "Ba Vì", "Chương Mỹ", "Sơn Tây"  # Sơn Tây là thị xã
]

project_names = data['Tên dự án'].drop_duplicates().to_list()

property_types = [
    "Căn hộ chung cư",
    "Chung cư mini, căn hộ dịch vụ",
    "Nhà riêng",
    "Nhà Biệt thự, liền kề",
    "Nhà mặt phố",
    "Shophouse, nhà phố thương mại",
    "Bán đất",
    "Bất động sản khác",
    "Trang trại, khu nghỉ dưỡng",
    "Condotel",
    "Kho, nhà xưởng"
]

segment_types = ['under_50', 'between_50_100', 'between_100_150', 'between_150_200', 'over_200']

for area_name in districts_hanoi:
    try:
        hPA = historyPriceOfArea(area_name)
        hPA.toJson()
        print('Thành công : ', area_name)
    except Exception as e:  # Bắt lỗi nếu có
        print('Lỗi:', e)
        print('Không thành công : ', area_name)
    
for project_name in project_names:
    try:
        hPP = historyPriceOfProject(project_name)
        hPP.toJson()
        print('Thành công : ', project_name)
    except Exception as e:  # Bắt lỗi nếu có
        print('Lỗi:', e)
        print('Không thành công : ', project_name)

for type_name in property_types:
    try:
        hPT = historyPriceOfType(type_name)
        hPT.toJson()
        print('Thành công : ', type_name)
    except Exception as e:  # Bắt lỗi nếu có
        print('Lỗi:', e)
        print('Không thành công : ', type_name)

for segment_type in segment_types:
    try:
        hPS = historyPriceOfSegment(segment_type)
        hPS.toJson()
        print('Thành công : ', segment_type)
    except Exception as e:  # Bắt lỗi nếu có
        print('Lỗi:', e)
        print('Không thành công : ', segment_type)
    