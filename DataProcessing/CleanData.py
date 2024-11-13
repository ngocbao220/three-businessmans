import pandas as pd
import numpy as np

# path_data_original = 'Data/originalData/data_project.csv'
# path_data_goal = 'Data/cleanedData/cleaned_data_project.csv'

path_data_original = 'Data/originalData/data_original.csv'
path_data_goal = 'Data/cleanedData/cleaned_data.csv'

# Drop duplicate elements
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

# Clean quận huyện xã phường
data['Quận/Huyện'] = data['Quận/Huyện'].str.replace(r'Quận|Huyện', '', regex=True).str.strip()
data['Xã/Phường'] = data['Xã/Phường'].str.replace(r'Xã|Phường|Thị trấn', '', regex=True).str.strip()

# Clean area Data
area = data['Diện tích']
area = area.str.replace(' m²', '').str.replace('.', '').str.replace(',', '.').astype(np.float32)

# Clean price Data

price = data['Mức giá']


wrong_form = price.str.contains('/m²', case=False, na=False)
cleaned_wrong_form = data.loc[wrong_form, 'Mức giá'].str.replace('/m²', '').str.replace(',', '.')
data.loc[wrong_form, 'Mức giá'] = cleaned_wrong_form

# Convert to price per square
price_area = price.str.contains('tỷ', case=False, na=False)
cleaned_price_area = data.loc[price_area, 'Mức giá'].str.replace(' tỷ', '').str.replace(',', '.').astype(np.float32)*1000
price_per_square = (cleaned_price_area / area[price_area])
data.loc[price_area, 'Mức giá'] = price_per_square

# Clean form
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

wrong_form = legal.str.contains('đang chờ sổ', case=False, na=False)
data.loc[wrong_form, 'Pháp lý'] = "Chưa có"

wrong_form = legal.str.contains(r'sổ|đầy đủ', case=False, na=False)
data.loc[wrong_form, 'Pháp lý'] = 'Đầy đủ'

# Clean furniture

furniture = data['Nội thất']
wrong_form = furniture.str.contains('.', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = data.loc[wrong_form, 'Nội thất'].str.replace('.', '')

wrong_form = furniture.str.contains(r'Cao cấp|đẹp|ngoại|semi', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = 'Cao cấp'

wrong_form = furniture.str.contains(r'cơ bản|nguyên bản|nhà mới|điều|mới', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = 'Cơ bản'

wrong_form = furniture.str.contains(r'Đầy đủ|full|toàn bộ|liên tường', case=False, na=False)
data.loc[wrong_form, 'Nội thất'] = 'Đầy đủ'

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
    'Diện tích (m²)': area,
    'Mức giá (triệu/m²)': price,
    'Số phòng ngủ (phòng)': bed_room,
    'Số toilet (phòng)': toilet_room,
    'Pháp lý': legal,
    'Nội thất': furniture,
    'Lịch sử giá': data['Lịch sử giá'],
    'Khoảng giá': data['Khoảng giá']
})

cleaned_data.to_csv(path_data_goal, index=False)