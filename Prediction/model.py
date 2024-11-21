import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

class Predictor:
    def __init__(self, time, prices):
        self.time = time
        self.prices = prices
        self.data = pd.DataFrame({"Time": time, "Price": prices})
        self.model = None
        self.encoded_time = None

    def standar(self):
        encoder = OneHotEncoder(sparse_output=False)
        self.encoded_time = encoder.fit_transform(self.data[['Time']])
        self.data['Time_Numeric'] = range(len(self.time))

    def learn(self):
        X = self.data[['Time_Numeric']].values
        y = self.data['Price'].values

        self.model = LinearRegression()
        self.model.fit(X, y)

    def getParameters(self):
        if self.model is None:
            raise ValueError("Model chưa được huấn luyện. Vui lòng gọi hàm 'learn()' trước.")
        a = self.model.coef_[0]
        b = self.model.intercept_
        return a, b

    def plotData(self):
        plt.figure(figsize=(8, 6))
        plt.plot(self.data['Time_Numeric'], self.data['Price'], color='blue')
        plt.title("Biểu đồ biến động giá")
        plt.xlabel("Mốc thời gian")
        plt.ylabel("Mức giá")
        plt.legend()
        plt.show()

    def plotRegression(self):
        a, b = self.getParameters()
        x_values = self.data['Time_Numeric']
        y_values = a * x_values + b

        plt.figure(figsize=(8, 6))
        plt.plot(x_values, self.data['Price'], color='blue')
        plt.plot(x_values, y_values, color='red')

        plt.annotate('', xy=(x_values.iloc[-1], y_values.iloc[-1]), xytext=(x_values.iloc[0], y_values.iloc[0]),
                     arrowprops=dict(facecolor='yellow', width=2, headwidth=10),
                     label="Mũi tên")
        plt.title("Biểu đồ biến động giá")
        plt.xlabel("Mốc thời gian")
        plt.ylabel("Giá nhà")
        plt.legend()
        plt.show()

time_data = ['T10/22', 'T11/22', 'T12/22', 'T01/23', 'T02/23', 'T03/23']
house_prices = [200, 120, 340, 300, 400, 500]

predictor = Predictor(time_data, house_prices)
predictor.standar()
predictor.learn()
predictor.plotData()
predictor.plotRegression()
