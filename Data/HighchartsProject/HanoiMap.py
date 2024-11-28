import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
import branca.colormap as cm

# Đọc dữ liệu bất động sản từ file CSV
data = pd.read_csv('../../Data/cleanedData/cleaned_data.csv')

# Loại bỏ các hàng có giá trị thiếu trong cột 'Quận/Huyện' và 'Mức giá'
heatmap_data = data.dropna(subset=['Quận/Huyện', 'Mức giá'])

# Chuyển đổi cột 'Mức giá' thành kiểu số
heatmap_data['Mức giá'] = pd.to_numeric(heatmap_data['Mức giá'], errors='coerce')

# Tính giá trung bình theo quận/huyện
avg_price_by_district = heatmap_data.groupby('Quận/Huyện')['Mức giá'].mean().reset_index()

# Đọc shapefile của Việt Nam và lọc lấy Hà Nội
vietnam_map = gpd.read_file('../../VisualizationData/Map/HaNoiMap')
hanoi_map = vietnam_map[vietnam_map['NAME_1'] == 'Hà Nội']
district_names = hanoi_map['NAME_2'].unique()
print("Danh sách các quận/huyện trong vietnam_map:")
for district in district_names:
    print(district)
# Ghép dữ liệu giá trung bình vào bản đồ Hà Nội
hanoi_map = hanoi_map.merge(avg_price_by_district, left_on='NAME_2', right_on='Quận/Huyện', how='left')

# Lấy Bounding Box của Hà Nội
minx, miny, maxx, maxy = hanoi_map.total_bounds

# Tạo một bản đồ nền bằng folium với nền mờ
m = folium.Map(
    tiles="CartoDB Positron",  # Nền mờ
    max_bounds=True,           # Giữ bản đồ trong giới hạn
    dragging=True,            # Không cho phép kéo bản đồ
    zoom_control=False,        # Tắt nút thu phóng
    scrollWheelZoom=True
          # Tắt thu phóng bằng cuộn chuột
)

# Cập nhật phạm vi hiển thị theo Bounding Box
m.fit_bounds([[miny, minx], [maxy, maxx]])

# Tạo colormap
colormap = cm.linear.YlOrRd_09.scale(hanoi_map['Mức giá'].min(), hanoi_map['Mức giá'].max())

# Chuyển đổi GeoDataFrame thành GeoJson và thêm vào bản đồ
geojson = folium.GeoJson(
    hanoi_map,
    style_function=lambda feature: {
        'fillColor': colormap(feature['properties']['Mức giá']) if feature['properties']['Mức giá'] else 'lightblue',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6,
    },
    tooltip=GeoJsonTooltip(
        fields=['NAME_2', 'Mức giá'],
        aliases=['Quận/Huyện', 'Giá trung bình (triệu VND)'],
        localize=True
    ),
    
).add_to(m)
colormap.height = 35
colormap.width = 350

# Thêm colormap vào bản đồ
colormap.add_to(m)


m.save('Hanoimap.html')
