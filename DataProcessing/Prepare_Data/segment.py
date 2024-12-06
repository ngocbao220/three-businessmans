import pandas as pd
import json
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
    area_name = re.sub(r'\s+', '_', area_name)  # Thay khoảng trắng

    return area_name

class segmentPriceOfArea:
    def __init__(self, area_name):
        if area_name != 'Hà Nội':
            total = data[(data['Quận/Huyện'] == area_name)].shape[0]
            self.under_50 = data[(data['Quận/Huyện'] == area_name) & (data['Mức giá'] < 50)].shape[0] / total * 100
            self.between_50_100 = data[(data['Quận/Huyện'] == area_name) & (data['Mức giá'] >= 50) & (data['Mức giá'] < 100)].shape[0] / total * 100
            self.between_100_150 = data[(data['Quận/Huyện'] == area_name) & (data['Mức giá'] >= 100) & (data['Mức giá'] < 150)].shape[0] / total * 100
            self.between_150_200 = data[(data['Quận/Huyện'] == area_name) & (data['Mức giá'] >= 150) & (data['Mức giá'] < 200)].shape[0] / total * 100
            self.over_200 = data[(data['Quận/Huyện'] == area_name) & (data['Mức giá'] > 200)].shape[0] / total * 100
        else:
            total = data.shape[0]
            self.under_50 = data[(data['Mức giá'] < 50)].shape[0] / total * 100
            self.between_50_100 = data[(data['Mức giá'] >= 50) & (data['Mức giá'] < 100)].shape[0] / total * 100
            self.between_100_150 = data[(data['Mức giá'] >= 100) & (data['Mức giá'] < 150)].shape[0] / total * 100
            self.between_150_200 = data[(data['Mức giá'] >= 150) & (data['Mức giá'] < 200)].shape[0] / total * 100
            self.over_200 = data[(data['Mức giá'] > 200)].shape[0] / total * 100
        self.area_name = area_name

    def toJson(self):
        # Chuyển dữ liệu cần thiết thành dictionary
        data_to_export = {
            "area_name": self.area_name,
            "under_50": self.under_50,
            "between_50_100": self.between_50_100,
            "between_100_150": self.between_100_150,
            "between_150_200": self.between_150_200,
            "over_200": self.over_200,
        }

        # Ghi vào file JSON
        with open(f"./Data/Json/Segment/area/{normalize_name(self.area_name)}.json", "w") as f:
            json.dump(data_to_export, f)

class segmentPriceOfProject:
    def __init__(self, project_name):
        total = data[data['Tên dự án'] == project_name].shape[0]
        self.under_50 = data[(data['Tên dự án'] == project_name) & (data['Mức giá'] < 50)].shape[0] / total * 100
        self.between_50_75 = data[(data['Tên dự án'] == project_name) & (data['Mức giá'] >= 50) & (data['Mức giá'] < 75)].shape[0] / total * 100
        self.between_75_100 = data[(data['Tên dự án'] == project_name) & (data['Mức giá'] >= 75) & (data['Mức giá'] < 100)].shape[0] / total * 100
        self.between_100_125 = data[(data['Tên dự án'] == project_name) & (data['Mức giá'] >= 100) & (data['Mức giá'] < 125)].shape[0] / total * 100
        self.over_125 = data[(data['Tên dự án'] == project_name) & (data['Mức giá'] >= 125)].shape[0] / total * 100
        self.project_name = project_name

    def toJson(self):
        # Chuyển dữ liệu cần thiết thành dictionary
        data_to_export = {
            "area_name": self.project_name,
            "under_50": self.under_50,
            "between_50_75": self.between_50_75,
            "between_75_100": self.between_75_100,
            "between_100_125": self.between_100_125,
            "over_125": self.over_125,
        }

        # Ghi vào file JSON
        with open(f"./Data/Json/Segment/project/{normalize_name(self.project_name)}.json", "w") as f:
            json.dump(data_to_export, f)

class segmentPriceOfType:
    def __init__(self, type_name):
        # Lọc dữ liệu theo loại hình
        total = data[data['Loại hình'] == type_name].shape[0]
        self.under_50 = data[(data['Loại hình'] == type_name) & (data['Mức giá'] < 50)].shape[0] / total * 100
        self.between_50_100 = data[(data['Loại hình'] == type_name) & (data['Mức giá'] >= 50) & (data['Mức giá'] < 100)].shape[0] / total * 100
        self.between_100_150 = data[(data['Loại hình'] == type_name) & (data['Mức giá'] >= 100) & (data['Mức giá'] < 150)].shape[0] / total * 100
        self.between_150_200 = data[(data['Loại hình'] == type_name) & (data['Mức giá'] >= 150) & (data['Mức giá'] < 200)].shape[0] / total * 100
        self.between_200_250 = data[(data['Loại hình'] == type_name) & (data['Mức giá'] >= 200) & (data['Mức giá'] < 250)].shape[0] / total * 100
        self.between_250_300 = data[(data['Loại hình'] == type_name) & (data['Mức giá'] >= 250) & (data['Mức giá'] < 300)].shape[0] / total * 100
        self.over_300 = data[(data['Loại hình'] == type_name) & (data['Mức giá'] > 300)].shape[0] / total * 100
        self.type_name = type_name

    def toJson(self):
        # Chuyển dữ liệu cần thiết thành dictionary
        data_to_export = {
            "type_name": self.type_name,
            "under_50": self.under_50,
            "between_50_100": self.between_50_100,
            "between_100_150": self.between_100_150,
            "between_150_200": self.between_150_200,
            "between_200_250": self.between_200_250,
            "between_250_300": self.between_250_300,
            "over_300": self.over_300,
        }

        # Ghi vào file JSON
        with open(f"./Data/Json/Segment/type/{normalize_name(self.type_name)}.json", "w",  encoding="utf-8") as f:
            json.dump(data_to_export, f, ensure_ascii=False, indent=4)

districts_hanoi = [
    'Hà Nội',"Ba Đình", "Hoàn Kiếm", "Hai Bà Trưng", "Đống Đa", "Tây Hồ", "Cầu Giấy",
    "Thanh Xuân", "Hoàng Mai", "Long Biên", "Hà Đông", "Bắc Từ Liêm", "Nam Từ Liêm",
    "Đan Phượng", "Đông Anh", "Gia Lâm", "Hoài Đức", "Mê Linh", "Mỹ Đức",
    "Phú Xuyên", "Phúc Thọ", "Quốc Oai", "Sóc Sơn", "Thạch Thất", "Thanh Oai",
    "Thanh Trì", "Thường Tín", "Ứng Hòa", "Ba Vì", "Chương Mỹ", "Sơn Tây"
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

# for area_name in districts_hanoi:
#     try:
#         sPA = segmentPriceOfArea(area_name)
#         sPA.toJson()
#         print('Thành công : ', area_name)
#     except Exception as e:
#         print('Lỗi: ', e)
#         print('Không thành công : ', area_name)

# for project_name in project_names:
#     try:
#         sPP = segmentPriceOfProject(project_name)
#         sPP.toJson()
#         print('Thành công : ', project_name)
#     except Exception as e:
#         print('Lỗi: ', e)
#         print('Không thành công : ', project_name)

for type in property_types:
    try:
        sPT = segmentPriceOfType(type)
        sPT.toJson()
        print('Thành công : ', type)
    except Exception as e:
        print('Lỗi: ', e)
        print('Không thành công : ', type)
