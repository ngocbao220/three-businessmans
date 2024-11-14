import pandas as pd

# Đọc file CSV
data = pd.read_csv('../Data/cleanedData/cleaned_data.csv')

# Tách các cột lịch sử giá theo từng tháng
data['Lịch sử giá'] = data['Lịch sử giá'].fillna("")  # Xử lý các giá trị trống nếu có
data_prices = data['Lịch sử giá'].str.extractall(r'Giá (T\d+/\d+): ([\d,.]+) tr/m²')
data_prices.index = data_prices.index.droplevel(1)
data_prices.columns = ['Thời gian', 'Giá']

# Chuyển đổi giá sang số float
data_prices['Giá'] = data_prices['Giá'].str.replace(',', '').astype(float)

# Gộp thông tin quận/huyện
data_combined = data[['Quận/Huyện']].join(data_prices)

# Tính giá trung bình cho từng thời gian của từng quận/huyện
average_prices = data_combined.groupby(['Quận/Huyện', 'Thời gian'])['Giá'].mean().reset_index()

# Lưu kết quả vào một file CSV khác
average_prices.to_csv('average_prices.csv', index=False)
