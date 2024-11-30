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

class countSegment:
    def __init__(self, type_segment, name):
        self.type_segment = type_segment
        self.name = name
        areas = ["Ba Đình", "Hoàn Kiếm", "Đống Đa", "Hai Bà Trưng", "Tây Hồ", "Cầu Giấy", "Thanh Xuân", "Hoàng Mai", "Long Biên", "Bắc Từ Liêm", "Nam Từ Liêm", "Hà Đông", "Gia Lâm", "Đông Anh", "Sóc Sơn", "Thanh Trì", "Thường Tín", "Phú Xuyên", "Ứng Hòa", "Mỹ Đức", "Chương Mỹ", "Thanh Oai", "Hoài Đức", "Đan Phượng", "Phúc Thọ", "Thạch Thất", "Quốc Oai", "Ba Vì", "Mê Linh", "Sơn Tây"]

        if name in areas:
            filtered_data = data[data['Quận/Huyện'] == name]
            self.category = 'area'
        elif name == 'Hà Nội':
            filtered_data = data
            self.category = 'area'
        else:
            filtered_data = data[data['Tên dự án'] == name]
            self.category = 'project'

        total = filtered_data.shape[0]

        if type_segment == 'Dưới 50 triệu':
            min_price = 0
            max_price = 50
        if type_segment == '50 đến 75 triệu':
            min_price = 50
            max_price = 175
        if type_segment == '75 đến 100 triệu':
            min_price = 75
            max_price = 100
        if type_segment == '100 đến 125 triệu':
            min_price = 100
            max_price = 125
        if type_segment == 'Trên 125 triệu':
            min_price = 125
            max_price = 1000000000

        self.totalApartment         = filtered_data[(filtered_data['Loại hình'] == 'Căn hộ chung cư') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalMiniApartment     = filtered_data[(filtered_data['Loại hình'] == 'Chung cư mini, căn hộ dịch vụ') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalHouse             = filtered_data[(filtered_data['Loại hình'] == 'Nhà riêng') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalTownhouse         = filtered_data[(filtered_data['Loại hình'] == 'Nhà Biệt thự, liền kề') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalStreetHouse       = filtered_data[(filtered_data['Loại hình'] == 'Nhà mặt phố') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalShophouse         = filtered_data[(filtered_data['Loại hình'] == 'Shophouse, nhà phố thương mại') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalProjectLand       = filtered_data[(filtered_data['Loại hình'] == 'Đất nền dự án') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalLand              = filtered_data[(filtered_data['Loại hình'] == 'Bán đất') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalFarmResort        = filtered_data[(filtered_data['Loại hình'] == 'Trang trại, khu nghỉ dưỡng') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalCondotel          = filtered_data[(filtered_data['Loại hình'] == 'Condotel') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalWarehouse         = filtered_data[(filtered_data['Loại hình'] == 'Kho, nhà xưởng') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]
        self.totalOrtherProperty    = filtered_data[(filtered_data['Loại hình'] == 'Bất động sản khác') & (filtered_data['Mức giá'] >= min_price) & (filtered_data['Mức giá'] < max_price)].shape[0]

        self.persentApartment       = float(self.totalApartment / total * 100)
        self.persentMiniApartment   = float(self.totalMiniApartment / total * 100)
        self.persentHouse           = float(self.totalHouse / total * 100)
        self.persentTownhouse       = float(self.totalTownhouse / total * 100)
        self.persentStreetHouse     = float(self.totalStreetHouse / total * 100)
        self.persentShophouse       = float(self.totalShophouse / total * 100)
        self.persentProjectLand     = float(self.totalProjectLand / total * 100)
        self.persentLand            = float(self.totalLand / total * 100)
        self.persentFarmResort      = float(self.totalFarmResort / total * 100)
        self.persentCondotel        = float(self.totalCondotel / total * 100)
        self.persentWarehouse       = float(self.totalWarehouse / total * 100)
        self.persentOrtherProperty  = float(self.totalOrtherProperty / total * 100)

    def toJson(self):
        # Chuyển dữ liệu cần thiết thành dictionary
        data_to_export = {
            "Apartment": self.totalApartment,
            "MiniApartment": self.totalMiniApartment,
            "House": self.totalHouse,
            "Townhouse": self.totalTownhouse,
            "StreetHouse": self.totalStreetHouse,
            "Shophouse": self.totalShophouse,
            "ProjectLand": self.totalProjectLand,
            "Land": self.totalLand,
            "FarmResort": self.totalFarmResort,
            "Condotel": self.totalCondotel,
            "Warehouse": self.totalWarehouse,
            "OrtherProperty": self.totalOrtherProperty
        }

        # Ghi vào file JSON
        if self.category == 'area':
            with open(f"./Data/Json/Segment/area/count/{normalize_name(self.name)}.json", "w") as f:
                json.dump(data_to_export, f)
        else:
            with open(f"./Data/Json/Segment/project/count/{normalize_name(self.name)}.json", "w") as f:
                json.dump(data_to_export, f)


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
