import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from folium import LayerControl
from branca.colormap import linear as cm
import json
import os

# HÀM HỖ TRỢ
def normalize_name(area_name):
    """Chuẩn hóa tên khu vực để lưu file."""
    import unicodedata
    import re
    area_name = unicodedata.normalize('NFD', area_name)
    area_name = ''.join(ch for ch in area_name if unicodedata.category(ch) != 'Mn')
    area_name = re.sub(r'\s+|, ', '_', area_name.lower().replace('đ', 'd').replace('-', ' '))
    return area_name

def add_colormap_to_layer(gdf, column, map_obj, layer_name, tooltip_fields, tooltip_aliases):
    """Thêm dữ liệu GeoJSON vào bản đồ với colormap, lưu dưới dạng một lớp."""
    colormap = cm.YlOrRd_09.scale(gdf[column].min(), gdf[column].max())
    geojson = folium.GeoJson(
        gdf,
        name=layer_name,  # Đặt tên lớp
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties'][column]) if feature['properties'][column] else 'white',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        },
        tooltip=GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_aliases, localize=True),
    )
    geojson.add_to(map_obj)

def create_base_map(bounds):
    """Tạo bản đồ nền dựa trên Bounding Box."""
    minx, miny, maxx, maxy = bounds
    m = folium.Map(
        tiles="CartoDB Positron",
        max_bounds=True,
        dragging=True,
        zoom_control=True,
        scrollWheelZoom=True,
    )
    m.fit_bounds([[miny, minx], [maxy, maxx]])
    return m

# ĐỌC DỮ LIỆU
data = pd.read_csv('./Data/cleanedData/cleaned_data_new.csv')
avg_price_by_ward = data.groupby('Xã/Phường')['Mức giá'].mean().reset_index()
avg_price_by_district = data.groupby('Quận/Huyện')['Mức giá'].mean().reset_index()

# Hàm tính biến động
def makeData(districts):
    data = pd.DataFrame(columns=['District', 'FTA_2_years', 'FTA_1_year', 'FTA_6_months'])
    for district in districts:
        json_path = f'./Data/Json/History_Price/area/{normalize_name(district)}.json'
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                district_data = json.load(file)
            amount_2 = round(
                ((district_data[1]['Giá T10/24'] / district_data[1]['Giá T10/22']) - 1) * 100, 2
            )
            amount_1 = round(
                ((district_data[1]['Giá T10/24'] / district_data[1]['Giá T10/23']) - 1) * 100, 2
            )
            amount_6 = round(
                ((district_data[1]['Giá T10/24'] / district_data[1]['Giá T5/24']) - 1) * 100, 2
            )
            new_row = pd.DataFrame({
                'District': [district],
                'FTA_2_years': [amount_2],
                'FTA_1_year': [amount_1],
                'FTA_6_months': [amount_6]
            })
            data = pd.concat([data, new_row], ignore_index=True)
        except (KeyError, IndexError, ZeroDivisionError, FileNotFoundError) as e:
            print(f"Lỗi với khu vực {district}: {e}")
            continue
    return data

# Danh sách quận/huyện
districts = [
    "Ba Đình", "Bắc Từ Liêm", "Cầu Giấy", "Chương Mỹ", "Đông Anh", "Đống Đa",
    "Gia Lâm", "Hà Đông", "Hai Bà Trưng", "Hà Nội", "Hoài Đức", "Hoàn Kiếm",
    "Hoàng Mai", "Long Biên", "Mê Linh", "Nam Từ Liêm", "Tây Hồ", "Thạch Thất",
    "Thanh Oai", "Thanh Trì", "Thanh Xuân"
]

fta_data = makeData(districts)

# Dữ liệu bản đồ
district_map = gpd.read_file('./Data/Map/district')
hanoi_gdf = district_map[district_map['NAME_1'] == 'Hà Nội']

# KẾT HỢP DỮ LIỆU GIÁ TRUNG BÌNH
hanoi_avg_price = hanoi_gdf.merge(avg_price_by_district, left_on='NAME_2', right_on='Quận/Huyện', how='left')

# KẾT HỢP DỮ LIỆU BIẾN ĐỘNG
hanoi_fluctuation = hanoi_gdf.merge(fta_data, left_on='NAME_2', right_on='District', how='left')

# Tạo bản đồ tổng quát Hà Nội
hanoi_map = create_base_map(hanoi_gdf.total_bounds)

# Lớp giá trung bình
add_colormap_to_layer(
    hanoi_avg_price, 'Mức giá', hanoi_map,
    'Giá trung bình',
    ['NAME_2', 'Mức giá'], ['Quận/Huyện', 'Giá trung bình (triệu VND)']
)

# Lớp biến động 2 năm
add_colormap_to_layer(
    hanoi_fluctuation, 'FTA_2_years', hanoi_map,
    'Biến động giá 2 năm',
    ['NAME_2', 'FTA_2_years'], ['Quận/Huyện', 'Biến động 2 năm (%)']
)

# Lớp biến động 1 năm
add_colormap_to_layer(
    hanoi_fluctuation, 'FTA_1_year', hanoi_map,
    'Biến động giá 1 năm',
    ['NAME_2', 'FTA_1_year'], ['Quận/Huyện', 'Biến động 1 năm (%)']
)

# Lớp biến động 6 tháng
add_colormap_to_layer(
    hanoi_fluctuation, 'FTA_6_months', hanoi_map,
    'Biến động giá 6 tháng',
    ['NAME_2', 'FTA_6_months'], ['Quận/Huyện', 'Biến động 6 tháng (%)']
)

# Thêm nút bật/tắt lớp
LayerControl().add_to(hanoi_map)

# LƯU FILE HTML
output_path = './HighchartsProject/html/data_for_map/ha_noi.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
hanoi_map.save(output_path)

print(f"Bản đồ Hà Nội đã được lưu tại: {output_path}")
