import pandas as pd
import csv
import re
import matplotlib.pyplot as plt
import json
import unicodedata


data_view_of_project_Path = './Data/originalData/data_project_view.csv'

dataView = pd.read_csv(data_view_of_project_Path)

class TopViewOfProject:
    def __init__(self):
        self.dataView = dataView
        self.top_10_view = None
    def topViewOfProject(self):
        top_10_projects = dataView.sort_values(by='Lượt xem', ascending=False).head(10)

        # Chuyển thành dictionary
        self.top_10_view = top_10_projects.set_index('Tên dự án')['Lượt xem'].to_dict()
        print(self.top_10_view)
    def toJson(self):
        self.topViewOfProject()
        data_to_export = self.top_10_view

        # Ghi vào file JSON
        with open(f"./Data/Json/Top_View_Of_Project/view_of_project.json", "w") as f:
            json.dump(data_to_export, f)

topView = TopViewOfProject()
topView.toJson()