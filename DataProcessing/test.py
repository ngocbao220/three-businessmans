import pandas as pd

# Đọc file CSV
data_new_Path = 'D:\\AI - năm hai\\Kì I\\LT xử lý dữ liệu\BTL\\three-businessmans\\Data\\originalData\\data_original_new.csv'

df = pd.read_csv(data_new_Path)

# Danh sách các quận/huyện cần loại bỏ
danh_sach_loai_bo = []

# Loại bỏ các bản ghi có Quận/Huyện nằm trong danh sách
df = df[~df['Quận/Huyện'].isin(danh_sach_loai_bo)]

# Ghi kết quả vào file CSV mới
df.to_csv(data_new_Path, index=False)

print("Đã loại bỏ các bản ghi và lưu vào file mới.")
