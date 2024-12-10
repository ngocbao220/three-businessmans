import pandas as pd
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
    
    def prediction(self):
        self.standar()
        self.learn()
        a, b = self.getParameters()

        return a * 26 + b

    def plotData(self):
        plt.figure(figsize=(13, 6))
        plt.plot(self.time, self.data['Price'], color='blue')
        plt.xlabel("Mốc thời gian")
        plt.ylabel("Mức giá")
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.legend()
        plt.show()

    def plotRegression(self):
        a, b = self.getParameters()
        x_values = self.data['Time_Numeric']
        y_values = a * x_values + b

        plt.figure(figsize=(13, 6))
        plt.plot(self.time, self.data['Price'], color='blue')
        plt.plot(x_values, y_values, color='red')

        plt.annotate('', xy=(x_values.iloc[-1], y_values.iloc[-1]), xytext=(x_values.iloc[0], y_values.iloc[0]),
                     arrowprops=dict(facecolor='yellow', width=2, headwidth=10),
                     label="Mũi tên")
        plt.xlabel("Mốc thời gian")
        plt.ylabel("Giá nhà")
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.legend()
        plt.show()

    def show(self):
        self.standar()
        self.learn()
        self.plotData()
        self.plotRegression()

time = ['T10/22', 'T11/22', 'T12/22', 'T1/23', 'T2/23', 'T3/23', 'T4/23', 'T5/23', 
'T6/23', 'T7/23', 'T8/23', 'T9/23', 'T10/23', 'T11/23', 'T12/23', 'T1/24', 
'T2/24', 'T3/24', 'T4/24', 'T5/24', 'T6/24', 'T7/24', 'T8/24', 'T9/24', 'T10/24']

price = [100.0, 98.0, 113.1, 104.5, 110.3, 105.2, 103.8, 100.0, 108.2, 106.4, 
110.6, 108.5, 121.8, 108.2, 114.7, 114.9, 108.3, 116.9, 140.0, 136.4, 
150.0, 148.0, 154.5, 161.1, 159.1]


p = Predictor(time, price)
p.standar()
p.learn()
p.plotData()
p.plotRegression()

print(p.prediction())
