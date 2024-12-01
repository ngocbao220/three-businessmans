import pandas as pd
import csv
import re
import matplotlib.pyplot as plt
import json

data_original_Path = './Data/cleanedData/cleaned_data_new.csv'
data_project_Path = './Data/cleanedData/cleaned_data_project.csv'

dataArea = pd.read_csv(data_original_Path)
dataProject = pd.read_csv(data_project_Path)


class numRealEstateArea:
    def __init__(self):
        self.dataNumOfTypeProperty = None
        self.number_of_classify = None
    def numRealEstate(self):
        self.number_of_classify = dataArea.groupby('Loại hình').size()
        #self.number_of_classify = self.number_of_classify.drop(['Bán đất', 'Chung cư mini, căn hộ dịch vụ','Condotel', 'Nhà mặt phố', 'Nhà riêng'])

        temp = self.number_of_classify["Bất động sản khác"]  # Lưu giá trị của hàng này
        self.number_of_classify = self.number_of_classify.drop("Bất động sản khác")  # Loại bỏ khỏi Series
        self.number_of_classify["Bất động sản khác"] = temp  # Thêm lại vào cuối
    def toJson(self):
        self.numRealEstate()
        data_to_export = self.number_of_classify.to_dict()
        print(data_to_export)
        # Ghi vào file JSON
        
        with open(f"./Data/Json/Number_Of_Type_Property/area.json", "w") as f:
            json.dump(data_to_export, f)

class numRealEstateProject:
    def __init__(self):
        self.dataNumOfTypeProperty = None
        self.number_of_classify = None
    def numRealEstate(self):
        self.number_of_classify = dataProject.groupby('Loại hình').size()
        self.number_of_classify = self.number_of_classify.drop(['Chung cư mini, căn hộ dịch vụ','Condotel', 'Nhà mặt phố', 'Nhà riêng'])

        temp = self.number_of_classify["Bất động sản khác"]  # Lưu giá trị của hàng này
        self.number_of_classify = self.number_of_classify.drop("Bất động sản khác")  # Loại bỏ khỏi Series
        self.number_of_classify["Bất động sản khác"] = temp  # Thêm lại vào cuối
    def toJson(self):
        self.numRealEstate()
        data_to_export = self.number_of_classify.to_dict()
        print(data_to_export)
        # Ghi vào file JSON
        
        with open(f"./Data/Json/Number_Of_Type_Property/project.json", "w") as f:
            json.dump(data_to_export, f)

sPA = numRealEstateArea()
sPA.toJson()

sPA = numRealEstateProject()
sPA.toJson()
