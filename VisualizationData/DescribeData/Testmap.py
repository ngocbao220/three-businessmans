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
vietnam_map = gpd.read_file('../Map/HaNoiMap')
hanoi_map = vietnam_map[vietnam_map['NAME_1'] == 'Hà Nội']

# Ghép dữ liệu giá trung bình vào bản đồ Hà Nội
hanoi_map = hanoi_map.merge(avg_price_by_district, left_on='NAME_2', right_on='Quận/Huyện', how='left')

# Lấy Bounding Box của Hà Nội
minx, miny, maxx, maxy = hanoi_map.total_bounds

# Tạo một bản đồ nền bằng folium với nền mờ
m = folium.Map(
    zoom_start=9,
    tiles="CartoDB Positron",  # Nền mờ
    max_bounds=True,           # Giữ bản đồ trong giới hạn
    dragging=False,            # Không cho phép kéo bản đồ
    zoom_control=False,        # Tắt nút thu phóng
    scrollWheelZoom=False      # Tắt thu phóng bằng cuộn chuột
)

# Cập nhật phạm vi hiển thị theo Bounding Box
m.fit_bounds([[miny, minx], [maxy, maxx]])

# Tạo colormap
colormap = cm.linear.YlOrRd_09.scale(hanoi_map['Mức giá'].min(), hanoi_map['Mức giá'].max())

# In ra bounding box để kiểm tra
print(f"Bounding Box: MinX={minx}, MinY={miny}, MaxX={maxx}, MaxY={maxy}")

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
    highlight_function=lambda feature: {
        'fillColor': 'yellow',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7
    }
).add_to(m)


# Thêm colormap vào bản đồ
colormap.add_to(m)

# Lưu và hiển thị bản đồ
m.save('map.html')