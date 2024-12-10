import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
import branca.colormap as cm
import unicodedata
import re
import os

# HÀM HỖ TRỢ
def normalize_name(area_name):
    """Chuẩn hóa tên khu vực để lưu file."""
    area_name = unicodedata.normalize('NFD', area_name)
    area_name = ''.join(ch for ch in area_name if unicodedata.category(ch) != 'Mn')
    area_name = re.sub(r'\s+|, ', '_', area_name.lower().replace('đ', 'd').replace('-', ' '))
    return area_name

def create_district_map(district_map, avg_price_by_ward, colormap):
    """
    Tạo bản đồ nhiệt cho quận/huyện từ GeoDataFrame đã lọc.
    """
    if district_map.empty:
        raise ValueError("Dữ liệu quận/huyện bị rỗng.")

    # Ghép dữ liệu giá trung bình
    district_map = district_map.merge(avg_price_by_ward, left_on='NAME_3', right_on='Xã/Phường', how='left')

    # Tính tọa độ trung tâm và bounding box
    district_center = [district_map.geometry.centroid.y.mean(), district_map.geometry.centroid.x.mean()]
    minx, miny, maxx, maxy = district_map.total_bounds

    # Tạo bản đồ nền
    m_district = folium.Map(
        location=district_center,
        tiles="CartoDB Positron",
        zoom_control=True,
        scrollWheelZoom=True
    )
    m_district.fit_bounds([[miny, minx], [maxy, maxx]])

    # Thêm GeoJson vào bản đồ
    folium.GeoJson(
        district_map,
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['Mức giá']) if feature['properties']['Mức giá'] else 'white',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        },
        tooltip=GeoJsonTooltip(
            fields=['NAME_3', 'Mức giá'],
            aliases=['Xã/Phường', 'Giá trung bình (triệu VND)'],
            localize=True
        ),
    ).add_to(m_district)

    # Thêm chú thích colormap
    colormap.caption = 'Giá trung bình (triệu VND)'
    colormap.add_to(m_district)

    return m_district

def insert_css(file_path):
    """
    Chèn CSS tùy chỉnh để xoay thanh màu.
    """
    custom_css = """
    <style>
        .legend {
          position: relative;
          transform: rotate(-90deg) translate(-60%, 580%);
          transform-origin: center;
          z-index: 10;
        }
    </style>
    """
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        if '</head>' in content:
            content = content.replace('</head>', f'{custom_css}</head>')
        file.seek(0)
        file.write(content)
        file.truncate()

# ĐỌC DỮ LIỆU
data = pd.read_csv('./Data/cleanedData/cleaned_data_new.csv')
avg_price_by_ward = data.groupby('Xã/Phường')['Mức giá'].mean().reset_index()

# Đọc shapefile và lọc dữ liệu Hà Nội
vietnam_map = gpd.read_file('./Data/Map/village')
hanoi_map = vietnam_map[vietnam_map['NAME_1'] == 'Hà Nội']

# Tạo colormap toàn cục
min_price = avg_price_by_ward['Mức giá'].min()
max_price = avg_price_by_ward['Mức giá'].max()

global_colormap = cm.LinearColormap(
    colors=['lightblue', 'yellow', 'orange', 'red'],  # Dải màu
    vmin=min_price,  # Giá trị nhỏ nhất
    vmax=max_price   # Giá trị lớn nhất
)

# Tạo thư mục lưu file HTML nếu chưa tồn tại
output_dir = './HighchartsProject/html/data_for_map/'
os.makedirs(output_dir, exist_ok=True)

# Lấy danh sách các quận/huyện
district_names = hanoi_map['NAME_2'].unique()

# Tạo bản đồ cho từng quận/huyện
for district_name in district_names:
    try:
        district_map = hanoi_map[hanoi_map['NAME_2'] == district_name].to_crs(epsg=4326)
        file_path = f'{output_dir}{normalize_name(district_name)}.html'
        map_output = create_district_map(district_map, avg_price_by_ward, global_colormap)
        map_output.save(file_path)
        insert_css(file_path)  # Chèn CSS để thanh màu nằm dọc
        print(f"Thành công: {district_name}")
    except Exception as e:
        print(f"Lỗi với {district_name}: {e}")
