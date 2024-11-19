import pandas as pd
import numpy as np

# path_data_original = 'Data/originalData/data_project.csv'
# path_data_goal = 'Data/cleanedData/cleaned_data_project.csv'

path_data_original = 'Data/originalData/data_original.csv'
path_data_goal = 'Data/cleanedData/cleaned_data.csv'

# Drop elements
data = pd.read_csv(path_data_original).copy()
data = data.drop(columns=['Mặt tiền', 'Hướng nhà', 'Hướng ban công', 'Thông tin khác'])
data = data.drop_duplicates()
data = data[data['Tỉnh/Thành phố'].str.contains('Hà Nội', case=False, na=False)].reset_index(drop=True)
data = data[~data['Chủ đầu tư'].str.contains('Đang cập nhật', case=False, na=False)].reset_index(drop=True)
data = data[~data['Tên dự án'].str.contains('Đang cập nhật', case=False, na=False)].reset_index(drop=True)
data = data[~data['Mức giá'].str.contains('Thỏa thuận', case=False, na=False)].reset_index(drop=True)
data = data[~data['Số phòng ngủ'].str.contains('Không có thông tin', case=False, na=False)].reset_index(drop=True)
data = data[~data['Số toilet'].str.contains('Không có thông tin', case=False, na=False)].reset_index(drop=True)
data = data[~data['Pháp lý'].str.contains('Không có thông tin', case=False, na=False)].reset_index(drop=True)
data = data[~data['Nội thất'].str.contains('Không có thông tin', case=False, na=False)].reset_index(drop=True)

# Clean Area
data['Quận/Huyện'] = data['Quận/Huyện'].str.replace(r'Quận|Huyện', '', regex=True).str.strip()
data['Xã/Phường'] = data['Xã/Phường'].str.replace(r'Xã|Phường|Thị trấn', '', regex=True).str.strip()

# Clean Square Data
area = data['Diện tích']
area = area.str.replace(' m²', '').str.replace('.', '').str.replace(',', '.').astype(np.float32)

# Clean Price Data
price = data['Mức giá']

wrong_form = price.str.contains('/m²', case=False, na=False)
cleaned_wrong_form = data.loc[wrong_form, 'Mức giá'].str.replace('/m²', '').str.replace(',', '.')
data.loc[wrong_form, 'Mức giá'] = cleaned_wrong_form

price_area = price.str.contains('tỷ', case=False, na=False)
cleaned_price_area = data.loc[price_area, 'Mức giá'].str.replace(' tỷ', '').str.replace(',', '.').astype(np.float32)*1000
price_per_square = (cleaned_price_area / area[price_area])
data.loc[price_area, 'Mức giá'] = price_per_square

wrong_form = price.str.contains(' triệu', case=False, na=False)
cleaned_wrong_form = data.loc[wrong_form, 'Mức giá'].str.replace(' triệu', '').str.replace(',', '.').astype(np.float32)
data.loc[wrong_form, 'Mức giá'] = cleaned_wrong_form

# Clean room
bed_room = data['Số phòng ngủ']
bed_room = bed_room.str.replace(' phòng', '').astype(np.float32)
toilet_room = data['Số toilet']
toilet_room = toilet_room.str.replace(' phòng', '').astype(np.float32)

# Clean legal
legal = data['Pháp lý']
wrong_form = legal.str.contains('HĐMB', case=False, na=False)
data.loc[wrong_form, 'Pháp lý'] = data.loc[wrong_form, 'Pháp lý'].str.replace('HĐMB', "Hợp đồng mua bán")

wrong_form = legal.str.contains('.', case=False, na=False)
data.loc[wrong_form, 'Pháp lý'] = data.loc[wrong_form, 'Pháp lý'].str.replace('.', '')

wrong_form = legal.str.contains('hợp đồng', case=False, na=False)
data.loc[wrong_form, 'Pháp lý'] = "Hợp đồng mua bán"

wrong_form = legal.str.contains('đang chờ sổ', case=False, na=False)
data.loc[wrong_form, 'Pháp lý'] = "Chưa có"

wrong_form = legal.str.contains(r'sổ|so|Sổ đỏ/ Sổ hồng|đầy đủ', case=False, na=False)
data.loc[wrong_form, 'Pháp lý'] = 'Đầy đủ'

# Clean furniture
furniture = data['Nội thất']
wrong_form = furniture.str.contains('.', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = data.loc[wrong_form, 'Nội thất'].str.replace('.', '')

wrong_form = furniture.str.contains(r'Cao cấp|cáo cấp|đẹp|ngoại|semi|hiện đại|sang|nhập khẩu|xịn|châu âu|tâm huyết|hien dai', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = 'Cao cấp'

wrong_form = furniture.str.contains(r'cơ bản|nguyên bản|nhà mới|điều|mới|thang máy|kèm nội thất|41518075|hầm chìm', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = 'Cơ bản'

wrong_form = furniture.str.contains(r'Đầy đủ|full|toàn bộ|liên tường|liền tường|đủ|cẩn thận|hoàn thiện nội thất', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = 'Đầy đủ'

wrong_form = furniture.str.contains(r'Xây thô|Thô', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = 'Không nội thất' 


# Clean project
project_name = data['Tên dự án']
wrong_form = project_name.str.contains('Không có thông tin', case=False, na=False)
data.loc[wrong_form, 'Tên dự án'] = "Tư nhân"

investment = data['Chủ đầu tư']
wrong_form = investment.str.contains('Không có thông tin', case=False, na=False)
data.loc[wrong_form, 'Chủ đầu tư'] = 'Tư nhân'

cleaned_data = pd.DataFrame({
    'Xã/Phường': data['Xã/Phường'],
    'Quận/Huyện': data['Quận/Huyện'],
    'Chủ đầu tư': data['Chủ đầu tư'],
    'Tên dự án': data['Tên dự án'],
    'Diện tích': area,
    'Mức giá': price,
    'Số phòng ngủ': bed_room,
    'Số toilet': toilet_room,
    'Pháp lý': legal,
    'Nội thất': furniture,
    'Lịch sử giá': data['Lịch sử giá'],
    'Khoảng giá': data['Khoảng giá']
})

# PRICE Encoding
month_price_path = 'Data/priceData/month_price.csv'
quarter_price_path = 'Data/priceData/quarter_price.csv'

history_price = pd.DataFrame(index=data.index)
price_data = cleaned_data[['Lịch sử giá', 'Khoảng giá']].copy()

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

cleaned_data.loc[month_indices, 'Lịch sử giá'] = 'M'
cleaned_data.loc[quarter_indices, 'Lịch sử giá'] = 'Q'
cleaned_data.loc[none_indices, 'Lịch sử giá'] = 'N'

cleaned_data.drop(columns=['Khoảng giá'], inplace=True)
cleaned_data.rename(columns={"Lịch sử giá" : "Mã lịch sử giá"}, inplace=True)

cleaned_data.to_csv(path_data_goal, index=False)
month_price.to_csv(month_price_path, index=True, index_label="index")
quarter_price.to_csv(quarter_price_path, index=True, index_label="index")