import pandas as pd
import json
import numpy as np
import os
import sys
import unicodedata
import re

data = pd.read_csv('./Data/cleanedData/cleaned_data_new.csv')

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
    area_name = re.sub(r'\s+|, ', '_', area_name)  # Thay khoảng trắng

    return area_name

class AreaCorrelation():
    def __init__(self, area_name) :
        self.area_name = area_name
        if (area_name != 'Hà Nội'):
            self.data = data[data['Quận/Huyện'] == area_name]
        else:
            self.data = data
    def getCorr(self):
        self.corr = self.data.loc[:,['Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất']].corr()
    def toJson(self):
        self.getCorr()
        corr_json= self.corr.to_json(orient='split')

        # Lưu vào file JSON
        with open(f'Data/Json/Correlation/area/{normalize_name(self.area_name)}.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(corr_json), f, ensure_ascii=False, indent=4)

class TypeCorrelation():
    def __init__(self, type_name) :
        self.type_name = type_name
        self.data = data[data['Loại hình'] == type_name]
    def getCorr(self):
        self.corr = self.data.loc[:,['Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất']].corr()
    def toJson(self):
        self.getCorr()
        corr_json= self.corr.to_json(orient='split')

        # Lưu vào file JSON
        with open(f'Data/Json/Correlation/type/{normalize_name(self.type_name)}.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(corr_json), f, ensure_ascii=False, indent=4)

class SegmentCorrelation():
    def __init__(self, type_segment) :
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
    def getCorr(self):
        self.corr = self.data.loc[:,['Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất']].corr()
    def toJson(self):
        self.getCorr()
        corr_json= self.corr.to_json(orient='split')

        # Lưu vào file JSON
        with open(f'Data/Json/Correlation/segment/{normalize_name(self.type_segment)}.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(corr_json), f, ensure_ascii=False, indent=4)

class ProjectCorrelation():
    def __init__(self, project_name) :
        self.project_name = project_name
        self.data = data[data['Tên dự án'] == project_name]
    def getCorr(self):
        self.corr = self.data.loc[:,['Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất']].corr()
    def toJson(self):
        self.getCorr()
        corr_json= self.corr.to_json(orient='split')

        # Lưu vào file JSON
        with open(f'Data/Json/Correlation/project/{normalize_name(self.project_name)}.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(corr_json), f, ensure_ascii=False, indent=4)

districts_hanoi = [
    'Hà Nội',"Ba Đình", "Hoàn Kiếm", "Hai Bà Trưng", "Đống Đa", "Tây Hồ", "Cầu Giấy",
    "Thanh Xuân", "Hoàng Mai", "Long Biên", "Hà Đông", "Bắc Từ Liêm", "Nam Từ Liêm",
    "Đan Phượng", "Đông Anh", "Gia Lâm", "Hoài Đức", "Mê Linh", "Mỹ Đức",
    "Phú Xuyên", "Phúc Thọ", "Quốc Oai", "Sóc Sơn", "Thạch Thất", "Thanh Oai",
    "Thanh Trì", "Thường Tín", "Ứng Hòa", "Ba Vì", "Chương Mỹ", "Sơn Tây"  # Sơn Tây là thị xã
]

project_names = data['Tên dự án'].drop_duplicates().to_list()

segment_names = ['under_50', 'between_50_100', 'between_100_150', 'between_150_200', 'over_200']

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

for area_name in districts_hanoi:
    try:
        aP = AreaCorrelation(area_name)
        aP.toJson()
        print('Thành công: ', area_name)
    except Exception as e:
        print('Không thành công: ', area_name)
        print('Lỗi:', e)

for project_name in project_names:
    try:
        pP = ProjectCorrelation(project_name)
        pP.toJson()
        print('Thành công: ', project_name)
    except Exception as e:
        print('Không thành công: ', project_name)
        print('Lỗi:', e)

for segment_name in segment_names:
    try:
        sP = SegmentCorrelation(segment_name)
        sP.toJson()
        print('Thành công: ', segment_name)
    except Exception as e:
        print('Không thành công: ', segment_name)
        print('Lỗi:', e)

for type_name in property_types:
    try:
        tP = TypeCorrelation(type_name)
        tP.toJson()
        print('Thành công: ', type_name)
    except Exception as e:
        print('Không thành công: ', type_name)
        print('Lỗi:', e)

