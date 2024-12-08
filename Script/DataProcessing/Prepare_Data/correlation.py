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
        if type_segment == 1:
            self.data = data[data['Mức giá'] < 100]
        elif type_segment == 2:
            self.data = data[(data['Mức giá'] >= 100) & (data['Mức giá'] < 200)]
        elif type_segment == 3:
            self.data = data[(data['Mức giá'] >= 200) & (data['Mức giá'] < 300)]
        elif type_segment == 4:
            self.data = data[(data['Mức giá'] >= 300)]
    def getCorr(self):
        self.corr = self.data.loc[:,['Diện tích', 'Mức giá', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất']].corr()
    def toJson(self):
        self.getCorr()
        corr_json= self.corr.to_json(orient='split')

        # Lưu vào file JSON
        with open(f'Data/Json/Correlation/segment/type{self.type_segment}.json', 'w', encoding='utf-8') as f:
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

area_names = ['Hà Nội', 'Nam Từ Liêm', 'Bắc Từ Liêm']
project_names = ['Vinhomes Ocean Park Gia Lâm', 'Khu đô thị Văn Khê']
segment_names = [1, 2, 3, 4]
type_names = ['Căn hộ chung cư', 'Nhà riêng', 'Chung cư mini, căn hộ dịch vụ', 'Nhà mặt phố']

for area_name in area_names:
    aP = AreaCorrelation(area_name)
    aP.toJson()

for project_name in project_names:
    pP = ProjectCorrelation(project_name)
    pP.toJson()
    
for segment_name in segment_names:
    sP = SegmentCorrelation(segment_name)
    sP.toJson()

for type_name in type_names:
    tP = TypeCorrelation(type_name)
    tP.toJson()
