import pandas as pd
import numpy as np
import unicodedata
import statistics
import re
import json
import os

dataArea = pd.read_csv('./Data/cleanedData/cleaned_data_new.csv')
dataProject = pd.read_csv('./Data/cleanedData/cleaned_data_project.csv')

#print(dataArea[dataArea['Quận/Huyện'] == 'Ba Đình'].index.to_list())
#print(priceAreaMonth['index'])

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


class VariabilityPrice():
    def __init__(self, type, name, time, type_segment) :
        self.type = type
        self.name = name
        self.time = time
        self.type_segment = type_segment
        self.standard_deviation = {}
        self.variance = {}
        
        if type == 'area' :
            self.data = dataArea[dataArea['Quận/Huyện'] == name]
        elif type == 'project' :
            self.data = dataProject[dataProject['Tên dự án'] == name]
        
        if name == 'Hà Nội':
            self.data = dataArea

        if type_segment == 'under_50':
            min_price = 0
            max_price = 50
        if type_segment == 'between_50_100':
            min_price = 50
            max_price = 100
        if type_segment == 'between_100_150':
            min_price = 150
            max_price = 100
        if type_segment == 'between_150_200':
            min_price = 150
            max_price = 200
        if type_segment == 'over_200':
            min_price = 200
            max_price = 1000000000

        if self.time == 'M':
            self.dictPrice = {'Giá T10/22': [], 'Giá T11/22': [], 'Giá T12/22': [],
                            'Giá T1/23': [], 'Giá T2/23': [], 'Giá T3/23': [],
                            'Giá T4/23': [], 'Giá T5/23': [], 'Giá T6/23': [],
                            'Giá T7/23': [], 'Giá T8/23': [], 'Giá T9/23': [],
                            'Giá T10/23': [], 'Giá T11/23': [], 'Giá T12/23': [],
                            'Giá T1/24': [], 'Giá T2/24': [], 'Giá T3/24': [],
                            'Giá T4/24': [], 'Giá T5/24': [], 'Giá T6/24': [],
                            'Giá T7/24': [], 'Giá T8/24': [], 'Giá T9/24': [],
                            'Giá T10/24': []
                            }
            self.dataPrice = pd.read_csv(f'./Data/priceData/{type}/month_price.csv')
            self.data = self.data[
                (self.data['Mã lịch sử giá'] == 'M') &
                (self.data['Mức giá'] >= min_price) &
                (self.data['Mức giá'] < max_price)
            ]

            self.dataPrice['index'] = self.dataPrice['index'].astype(int)

        else:
            self.dictPrice = {'Giá Q4/22': [], 'Giá Q1/23': [], 'Giá Q2/23': [],
                            'Giá Q3/23': [], 'Giá Q4/23': [], 'Giá Q1/24': [],
                            'Giá Q2/24': [], 'Giá Q3/24': [], 'Giá Q4/24': []
                            }
            self.dataPrice = pd.read_csv(f'./Data/priceData/{type}/quarter_price.csv')
            self.data = self.data[
                (self.data['Mã lịch sử giá'] == 'Q') &
                (self.data['Mức giá'] >= min_price) &
                (self.data['Mức giá'] < max_price)
            ]

            self.dataPrice['index'] = self.dataPrice['index'].astype(int)

        self.firstIndex = self.data.index[0]
        self.lastIndex = self.data.index[-1]

    def getPrice(self):
        for i in range(self.firstIndex, self.lastIndex + 1):
            rows = self.dataPrice[self.dataPrice['index'] == i]
            rows = rows.drop(columns=['index'])
            
            for index, row in rows.iterrows():
                for col in rows.columns:
                    if col != 'index':
                        value = row[col]
                        if isinstance(value, str):
                            # Tách chuỗi và lấy phần thứ 2 (index 1)
                            self.dictPrice[col].append(float(value.split()[1]))
                        
                                
    def caculate(self):
        self.getPrice()
        for col in self.dictPrice.keys():
            self.standard_deviation[col] = statistics.stdev(self.dictPrice[col])
            self.variance[col] = statistics.variance(self.dictPrice[col])
        

    def toJson(self):
        self.caculate()
        with open(f"./Data/Json/Std_And_Variance/Std/{self.type}/{normalize_name(self.name)}/{self.type_segment}.json", "w") as f:
            json.dump(self.standard_deviation, f)

        with open(f"./Data/Json/Std_And_Variance/Variance/{self.type}/{normalize_name(self.name)}/{self.type_segment}.json", "w") as f:
            json.dump(self.variance, f)


districts_hanoi = [
    'Hà Nội',"Ba Đình", "Hoàn Kiếm", "Hai Bà Trưng", "Đống Đa", "Tây Hồ", "Cầu Giấy",
    "Thanh Xuân", "Hoàng Mai", "Long Biên", "Hà Đông", "Bắc Từ Liêm", "Nam Từ Liêm",
    "Đan Phượng", "Đông Anh", "Gia Lâm", "Hoài Đức", "Mê Linh", "Mỹ Đức",
    "Phú Xuyên", "Phúc Thọ", "Quốc Oai", "Sóc Sơn", "Thạch Thất", "Thanh Oai",
    "Thanh Trì", "Thường Tín", "Ứng Hòa", "Ba Vì", "Chương Mỹ", "Sơn Tây"
] 

project_names = dataProject['Tên dự án'].drop_duplicates().to_list()

segmentPrices = {'under_50', 'between_50_100', 'between_100_150', 'between_150_200', 'over_200'}

# for area_name in districts_hanoi:
#     districtPath1 = f'./Data/Json/Std_And_Variance/Std/area/{normalize_name(area_name)}'
#     os.makedirs(districtPath1, exist_ok=True)
#     districtPath2 = f'./Data/Json/Std_And_Variance/Variance/area/{normalize_name(area_name)}'
#     os.makedirs(districtPath2, exist_ok=True)
#     for segmentPrice in segmentPrices:
#         try:
#             sPA = VariabilityPrice('area', area_name, 'M', segmentPrice)
#             sPA.toJson()
#             print('Thành công : ', area_name)
#         except Exception as e:
#             print('Lỗi: ', e)
#             print('Không thành công : ', area_name)

for project_name in project_names:
    Path1 = f'./Data/Json/Std_And_Variance/Std/project/{normalize_name(project_name)}'
    os.makedirs(Path1, exist_ok=True)
    Path2 = f'./Data/Json/Std_And_Variance/Variance/project/{normalize_name(project_name)}'
    os.makedirs(Path2, exist_ok=True)
    for segmentPrice in segmentPrices:
        try:
            sPP = VariabilityPrice('project', project_name, 'M', segmentPrice)
            sPP.toJson()
            print('Thành công : ', project_name)
        except Exception as e:
            print('Lỗi: ', e)
            print('Không thành công : ', project_name)




    
        
        

    
