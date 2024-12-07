import pandas as pd

# Đọc dữ liệu từ hai file CSV
file1 = pd.read_csv('Data/originalData/data_project_only.csv', encoding='utf-8')
file2 = pd.read_csv('Data/originalData/data_project_view.csv', encoding='utf-8')
htmlPath = 'HighchartsProject/listProject.html'

# Chuẩn hóa tên cột
file1.columns = file1.columns.str.strip()
file2.columns = file2.columns.str.strip()



# Gộp dữ liệu bằng cột "Tên dự án"
merged_data = pd.merge(file1, file2, on='Tên dự án', how='inner')

# Kiểm tra số lượng dự án gộp được
print(f"Số lượng dự án gộp được: {len(merged_data)}")

# Lọc các cột cần thiết
result = merged_data[['Tên dự án', 'Chủ đầu tư', 'Lượt xem', 'Quận/Huyện', 'Pháp lý']]
result = result.sort_values(by='Lượt xem', ascending=False)
# Tạo danh sách thẻ HTML
html_content = '<!DOCTYPE html>\n<html>\n<head>\n<title>Danh sách dự án</title>\n<style>\n'
html_content += '.project-card { border: 1px solid #ccc; padding: 10px; margin: 10px; border-radius: 5px; } \n'
html_content += '.project-card h2 { margin: 0; color: #007BFF; } \n'
html_content += '</style>\n</head>\n<body>\n'

# Lặp qua các dòng dữ liệu và tạo thẻ HTML
for _, row in result.iterrows():
    html_content += f'''
    <div class="project-card">
        <h2 style="display: inline-block; margin-right: 10px;">Tên dự án: {row['Tên dự án']}</h2>
        <p style="display: inline-block;">Lượt xem: {row['Lượt xem']}</p>
        <p>Chủ đầu tư: {row['Chủ đầu tư']}</p>
        <p>Quận/Huyện: {row['Quận/Huyện']}</p>
        <p>Pháp lý: {row['Pháp lý']}</p>
    </div>
    '''

# Kết thúc file HTML
html_content += '\n</body>\n</html>'

# Ghi nội dung HTML vào file
with open(htmlPath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("File HTML đã được tạo thành công!")