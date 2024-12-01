import pandas as pd
import csv
import re
import matplotlib.pyplot as plt
import json

data_original_Path = './Data/cleanedData/cleaned_data_new.csv'
data_project_Path = './Data/cleanedData/cleaned_data_project.csv'

dataArea = pd.read_csv(data_original_Path)
dataProject = pd.read_csv(data_project_Path)

class meanPriceOfType:
    def __init__(self, type_name) :
        self.type_name = type_name
        if type_name == 'area':
            self.data = dataArea
        elif type_name == 'project':
            self.data = dataProject
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
        
        key_to_drop = 'Bất động sản khác'
        value = self.avg_price.pop(key_to_drop)
        self.avg_price[key_to_drop] = value

    def toJson(self):
        self.caculateMean()
        data_to_export = self.avg_price
        #print(data_to_export)

        # Ghi vào file JSON
        with open(f"./Data/Json/Mean_Price/{self.type_name}.json", "w") as f:
            json.dump(data_to_export, f)

sPa = meanPriceOfType('area')
sPa.toJson()

sPa = meanPriceOfType('project')
sPa.toJson()