import pandas as pd

# Đọc dữ liệu từ file CSV
file_path = 'Data/cleanedData/cleaned_data_project.csv'  # Thay bằng đường dẫn thực tế của bạn
data = pd.read_csv(file_path, encoding='utf-8')

file_lowest_path = 'Data/originalData/data_lowest_price_pro.csv'  # Thay bằng đường dẫn thực tế của bạn

# Chuẩn hóa tên cột để tránh lỗi
data.columns = data.columns.str.strip()

# Đảm bảo cột 'Mức giá' là dạng số
data['Mức giá'] = pd.to_numeric(data['Mức giá'], errors='coerce')

# Loại bỏ các hàng có giá trị NaN trong cột 'Tên dự án' hoặc 'Mức giá'
data = data.dropna(subset=['Tên dự án', 'Mức giá'])

# Lọc ra giá thấp nhất cho từng tên dự án
result = data.loc[data.groupby('Tên dự án')['Mức giá'].idxmin()]

# Làm tròn 'Mức giá' đến 2 chữ số thập phân
result['Mức giá'] = result['Mức giá'].round(2)

# Chỉ giữ lại hai cột 'Tên dự án' và 'Mức giá'
result = result[['Tên dự án', 'Mức giá']]

# Xuất ra file mới hoặc in kết quả
result.to_csv(file_lowest_path, index=False, encoding='utf-8')
print(result)
