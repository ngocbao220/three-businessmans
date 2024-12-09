import pandas as pd
import ast

# Đọc dữ liệu từ hai file CSV
file1 = pd.read_csv('Data/originalData/data_project_only.csv', encoding='utf-8')
file2 = pd.read_csv('Data/originalData/data_project_view.csv', encoding='utf-8')
file3 = pd.read_csv('Data/originalData/data_lowest_price_pro.csv', encoding='utf-8')
htmlPath = 'HighchartsProject/addInfoProject.html'

# Chuẩn hóa tên cột
file1.columns = file1.columns.str.strip()
file2.columns = file2.columns.str.strip()

# Gộp file1 và file2 dựa trên 'Tên dự án'
merged_data_1 = pd.merge(file1, file2, on='Tên dự án', how='inner')

# Gộp kết quả với file3
merged_data = pd.merge(merged_data_1, file3, on='Tên dự án', how='inner')

print(merged_data.columns)
# Kiểm tra số lượng dự án gộp được
print(f"Số lượng dự án gộp được: {len(merged_data)}")

# Lọc các cột cần thiết
result = merged_data[['Tên dự án', 'Chủ đầu tư', 'Lượt xem', 'Quận/Huyện', 'Pháp lý','Diện tích','Số căn hộ', 'Số tòa', 'Mức giá']]
result = result.sort_values(by='Lượt xem', ascending=False)

# Tạo danh sách thẻ HTML
# Mở đầu file HTML
# Phần mở đầu file HTML
html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Danh sách dự án</title>
    <style>
        .project-card-2 {
            border: 1px solid #ccc;
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .project-card-2 p {
            margin: 5px 0;
        }
    </style>
</head>
<body>
'''

# Lặp qua các dòng dữ liệu và tạo thẻ HTML
for _, row in result.iterrows():
    html_content += f'''
    <div class="project-card-2">
        <h2>{row['Tên dự án']}</h2>
        <p>Chủ đầu tư: {row['Chủ đầu tư']}</p>
        <p>Lượt xem: {row['Lượt xem']}</p>
        <p>Quận/Huyện: {row['Quận/Huyện']}</p>
        <p>Pháp lý: {row['Pháp lý']}</p>
        <p>Diện tích: {row['Diện tích']}</p>
        <p>Số căn hộ: {row['Số căn hộ']}</p>
        <p>Số tòa: {row['Số tòa']}</p>
        <p>Mức giá: {row['Mức giá']}</p>
    </div>
    '''

# Kết thúc file HTML
html_content += '''
</body>
</html>
'''

# Ghi nội dung HTML vào file
with open(htmlPath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("File HTML đã được tạo thành công!")
