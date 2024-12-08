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

class numRealEstateArea:
    def __init__(self, area_name):
        self.area_name = area_name
        if (area_name == 'Hà Nội'):
            self.data = dataArea
        else:
            self.data = dataArea[dataArea['Quận/Huyện'] == area_name]

        self.number_of_classify = None
    def numRealEstate(self):
        self.number_of_classify = self.data.groupby('Loại hình').size()
        #self.number_of_classify = self.number_of_classify.drop(['Bán đất', 'Chung cư mini, căn hộ dịch vụ','Condotel', 'Nhà mặt phố', 'Nhà riêng'])
        if 'Bất động sản khác' in self.number_of_classify:
            temp = self.number_of_classify["Bất động sản khác"]  # Lưu giá trị của hàng này
            self.number_of_classify = self.number_of_classify.drop("Bất động sản khác")  # Loại bỏ khỏi Series
            self.number_of_classify["Bất động sản khác"] = temp  # Thêm lại vào cuối
    def toJson(self):
        self.numRealEstate()
        data_to_export = self.number_of_classify.to_dict()
        print(data_to_export)
        # Ghi vào file JSON
        
        with open(f"./Data/Json/Number_Of_Type_Property/area/{normalize_name(self.area_name)}.json", "w") as f:
            json.dump(data_to_export, f)

class numRealEstateProject:
    def __init__(self, project_name):
        self.project_name = project_name
        self.data = dataProject[dataProject['Tên dự án'] == project_name]
        self.number_of_classify = None
    def numRealEstate(self):
        self.number_of_classify = self.data.groupby('Loại hình').size()

        if 'Bất động sản khác' in self.number_of_classify:
            temp = self.number_of_classify["Bất động sản khác"]  # Lưu giá trị của hàng này
            self.number_of_classify = self.number_of_classify.drop("Bất động sản khác")  # Loại bỏ khỏi Series
            self.number_of_classify["Bất động sản khác"] = temp  # Thêm lại vào cuối
    def toJson(self):
        self.numRealEstate()
        data_to_export = self.number_of_classify.to_dict()
        print(data_to_export)
        # Ghi vào file JSON
        
        with open(f"./Data/Json/Number_Of_Type_Property/project/{normalize_name(self.project_name)}.json", "w") as f:
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
    sPA = numRealEstateArea(area_name)
    sPA.toJson()

for project_name in project_names:
    sPP = numRealEstateProject(project_name)
    sPP.toJson()
