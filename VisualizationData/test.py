import pandas as pd

month_price_path = 'Data/priceData/month_price.csv'
quarter_price_path = 'Data/priceData/quarter_price.csv'

data = pd.read_csv('Data/standardizedData/standardized_data.csv')
month_price = pd.read_csv(month_price_path)
quarter_price = pd.read_csv(quarter_price_path)

index = 12
code = data.loc[index, 'Mã lịch sử giá']

if code == 'M':
    price = month_price[month_price['index'] == index].dropna(axis=1).drop(columns=['index']).squeeze()
elif code == 'Q':
    price = quarter_price[quarter_price['index'] == index].dropna(axis=1).drop(columns=['index']).squeeze()
else:
    price = "Không có thông tin"

print(price)