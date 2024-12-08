import pandas as pd
import ast

# Đọc dữ liệu từ hai file CSV
file1 = pd.read_csv('Data/originalData/data_project_only.csv', encoding='utf-8')
file2 = pd.read_csv('Data/originalData/data_project_view.csv', encoding='utf-8')
htmlPath = 'HighchartsProject/addInfoProject.html'

# Chuẩn hóa tên cột
file1.columns = file1.columns.str.strip()
file2.columns = file2.columns.str.strip()



# Gộp dữ liệu bằng cột "Tên dự án"
merged_data = pd.merge(file1, file2, on='Tên dự án', how='inner')

# Kiểm tra số lượng dự án gộp được
print(f"Số lượng dự án gộp được: {len(merged_data)}")

# Lọc các cột cần thiết
result = merged_data[['Tên dự án', 'Chủ đầu tư', 'Lượt xem', 'Quận/Huyện', 'Pháp lý','Diện tích','Số căn hộ', 'Số tòa', 'Tiện ích']]
result = result.sort_values(by='Lượt xem', ascending=False)

if 'Tiện ích' in result.columns:
    result['Tiện ích'] = result['Tiện ích'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') and x.endswith(']') else x
    )

# Chuyển danh sách thành chuỗi, loại bỏ phần tử rỗng nếu có
result['Tiện ích'] = result['Tiện ích'].apply(
    lambda x: ', '.join([i for i in x if i]) if isinstance(x, list) else x
)
# Tạo danh sách thẻ HTML
# Mở đầu file HTML
html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Danh sách dự án</title>
    <style>
        .project-card {
            border: 1px solid #ccc;
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            position: relative;
        }
        .project-card h2 {
            margin: 0;
            color: #007BFF;
        }
        .details {
            display: none;
            margin-top: 10px;
        }
        .toggle-button {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            cursor: pointer;
        }
    </style>
    <script>
        function toggleDetails(button) {
            const details = button.parentElement.querySelector('.details');
            if (details.style.display === 'none' || details.style.display === '') {
                details.style.display = 'block';
                button.textContent = 'Thu gọn';
            } else {
                details.style.display = 'none';
                button.textContent = 'Chi tiết';
            }
        }
    </script>
</head>
<body>
'''

# Lặp qua các dòng dữ liệu và tạo thẻ HTML
for _, row in result.iterrows():
    html_content += f'''
    <div class="project-card-2">
        <p>Diện tích: {row['Diện tích']}</p>
        <p>Số căn hộ: {row['Số căn hộ']}</p>
        <p>Số tòa: {row['Số tòa']}</p>
        <p>Tiện ích: {row['Tiện ích']}</p>
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
