import pandas as pd

# path_data_original = 'Data/cleanedData/cleaned_data_project.csv'
# path_data_goal = 'Data/standardizedData/standardized_data_project.csv'

path_data_original = 'Data/cleanedData/cleaned_data.csv'
path_data_goal = 'Data/standardizedData/standardized_data.csv'

month_price_path = 'Data/priceData/month_price.csv'
quarter_price_path = 'Data/priceData/quarter_price.csv'

data = pd.read_csv(path_data_original).copy()

# standardization Price

history_price = pd.DataFrame(index=data.index)
price_data = data[['Lịch sử giá', 'Khoảng giá']].copy()

for idx, (history, price_range_str) in price_data.iterrows():
    entries = history.split('; ')
    price_ranges = price_range_str.split('; ')
    
    for i, entry in enumerate(entries):
        try:
            period, price = entry.split(': ')
            price_value = float(price.replace(' tr/m²', '').replace(',', '.'))
            
            min_price, max_price = price_ranges[i].split()
            min_value = float(min_price.replace(',', '.'))
            max_value = float(max_price.replace(',', '.'))

            history_price.loc[idx, period.strip()] = f"{min_value} {price_value} {max_value}"
            
        except:
            pass

month_price = history_price[history_price['Giá Q3/24'].isna() & history_price['Giá T10/24'].notna()].drop(
    columns=['Giá Q3/22', 'Giá Q4/22', 'Giá Q1/23', 'Giá Q2/23', 'Giá Q3/23', 'Giá Q4/23', 'Giá Q1/24', 'Giá Q2/24', 'Giá Q3/24']
)

quarter_price = history_price[history_price['Giá Q3/24'].notna()].drop(
    columns=['Giá T10/22', 'Giá T11/22', 'Giá T12/22', 'Giá T1/23', 'Giá T2/23', 'Giá T3/23', 'Giá T4/23', 'Giá T5/23', 'Giá T6/23', 'Giá T7/23', 'Giá T8/23', 'Giá T9/23', 'Giá T10/23', 'Giá T11/23', 'Giá T12/23', 'Giá T1/24', 'Giá T2/24', 'Giá T3/24', 'Giá T4/24', 'Giá T5/24', 'Giá T6/24', 'Giá T7/24', 'Giá T8/24', 'Giá T9/24', 'Giá T10/24']
)

none_price = history_price[history_price['Giá Q3/24'].isna() & history_price['Giá T10/24'].isna()]

month_indices = month_price.index
quarter_indices = quarter_price.index
none_indices = none_price.index

data.loc[month_indices, 'Lịch sử giá'] = 'M'
data.loc[quarter_indices, 'Lịch sử giá'] = 'Q'
data.loc[none_indices, 'Lịch sử giá'] = 'N'

data.drop(columns=['Khoảng giá'], inplace=True)
data.rename(columns={"Lịch sử giá" : "Mã lịch sử giá"}, inplace=True)

data.to_csv(path_data_goal, index=False)
month_price.to_csv(month_price_path, index=True, index_label="index")
quarter_price.to_csv(quarter_price_path, index=True, index_label="index")
