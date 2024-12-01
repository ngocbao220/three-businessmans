import pandas as pd
import csv
import re
import matplotlib.pyplot as plt
import json
import unicodedata

data_original_Path = './Data/cleanedData/cleaned_data_new.csv'
data_project_Path = './Data/cleanedData/cleaned_data_project.csv'

dataArea = pd.read_csv(data_original_Path)
dataProject = pd.read_csv(data_project_Path)

def normalize_name(area_name):
    # Bỏ dấu tiếng Việt
    area_name = unicodedata.normalize('NFD', area_name)
    area_name = ''.join(ch for ch in area_name if unicodedata.category(ch) != 'Mn')
    
    area_name = area_name.replace('đ', 'd')
    # Chuyển tất cả sang chữ thường
    area_name = area_name.lower()

    # Thay dấu cách và các ký tự không hợp lệ bằng dấu gạch dưới
    area_name = re.sub(r'\s+', '_', area_name)  # Thay khoảng trắng

    return area_name

class meanPriceOfType:
    def __init__(self, type_name, name) :
        self.type_name = type_name
        self.name = name
        if type_name == 'area':
            if name == 'Hà Nội' :
                self.data = dataArea
            else :
                self.data = dataArea[dataArea['Quận/Huyện'] == name]
        elif type_name == 'project':
            self.data = dataProject[dataArea['Tên dự án'] == name]
    def caculateMean(self) :
        result = [(row['Loại hình'], row['Mức giá']) 
          for _, row in self.data.iterrows()
        ]
        total_price = {}
        count_classify = {}

        # Chuyển thành định dạng chuỗi như bạn yêu cầu
        for aclassify, last_price in result:
            if aclassify in total_price:
                total_price[aclassify] += float(last_price)
                count_classify[aclassify] += 1
            else:
                total_price[aclassify] = float(last_price)
                count_classify[aclassify] = 1

        self.avg_price = {
            key: (total_price[key] / count_classify[key]) if count_classify[key] > 0 else 0
            for key in total_price.keys()
        }
        
        if 'Bất động sản khác' in self.avg_price:
            key_to_drop = 'Bất động sản khác'
            value = self.avg_price.pop(key_to_drop)
            self.avg_price[key_to_drop] = value 

    def toJson(self):
        self.caculateMean()
        data_to_export = self.avg_price
        #print(data_to_export)

        # Ghi vào file JSON
        with open(f"./Data/Json/Mean_Price/{self.type_name}/{normalize_name(self.name)}.json", "w") as f:
            json.dump(data_to_export, f)


districts_hanoi = [
    'Hà Nội',"Ba Đình", "Hoàn Kiếm", "Hai Bà Trưng", "Đống Đa", "Tây Hồ", "Cầu Giấy",
    "Thanh Xuân", "Hoàng Mai", "Long Biên", "Hà Đông", "Bắc Từ Liêm", "Nam Từ Liêm",
    "Đan Phượng", "Đông Anh", "Gia Lâm", "Hoài Đức", "Mê Linh", "Mỹ Đức",
    "Phú Xuyên", "Phúc Thọ", "Quốc Oai", "Sóc Sơn", "Thạch Thất", "Thanh Oai",
    "Thanh Trì", "Thường Tín", "Ứng Hòa", "Ba Vì", "Chương Mỹ", "Sơn Tây"
] 
project_names = dataProject['Tên dự án'].drop_duplicates().to_list()

for area_name in districts_hanoi:
    sPA = meanPriceOfType('area', area_name)
    sPA.toJson()

for project_name in project_names:
    sPP = meanPriceOfType('project', project_name)
    sPP.toJson()