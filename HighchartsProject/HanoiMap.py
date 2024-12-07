import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
import branca.colormap as cm

# Đọc dữ liệu bất động sản từ file CSV
data = pd.read_csv('../Data/cleanedData/cleaned_data_new.csv')

# Loại bỏ các hàng có giá trị thiếu trong cột 'Quận/Huyện' và 'Mức giá'
heatmap_data = data.dropna(subset=['Quận/Huyện', 'Mức giá'])

# Chuyển đổi cột 'Mức giá' thành kiểu số
heatmap_data['Mức giá'] = pd.to_numeric(heatmap_data['Mức giá'], errors='coerce')

# Tính giá trung bình theo quận/huyện
avg_price_by_district = heatmap_data.groupby('Quận/Huyện')['Mức giá'].mean().reset_index()

# Đọc shapefile của Việt Nam và lọc lấy Hà Nội
vietnam_map = gpd.read_file('../VisualizationData/Map/HaNoiMap')
hanoi_map = vietnam_map[vietnam_map['NAME_1'] == 'Hà Nội']

# Ghép dữ liệu giá trung bình vào bản đồ Hà Nội
hanoi_map = hanoi_map.merge(avg_price_by_district, left_on='NAME_2', right_on='Quận/Huyện', how='left')

# Lấy Bounding Box của Hà Nội
minx, miny, maxx, maxy = hanoi_map.total_bounds
colormap = cm.linear.YlOrRd_09.scale(hanoi_map['Mức giá'].min(), hanoi_map['Mức giá'].max())

# Tạo một bản đồ nền bằng folium với nền mờ
# Tạo bản đồ với các thiết lập như trước
m = folium.Map(
    zoom_start=9,
    tiles=None,  # Không sử dụng lớp nền mặc định
    max_bounds=True,
    dragging=True,
    zoom_control=False,
    scrollWheelZoom=True,
)

expansion_factor = 0.5  # Điều chỉnh hệ số mở rộng (đơn vị là độ)
bounds = [
    [miny - expansion_factor, minx - expansion_factor],  # Góc dưới cùng bên trái
    [maxy + expansion_factor, maxx + expansion_factor],  # Góc trên cùng bên phải
]
folium.Rectangle(
    bounds=bounds,
    color=None,
    fill=True,
    fill_color='#f48b4a',
    fill_opacity=1,
).add_to(m)

# Thêm lớp bản đồ nền mờ (nếu cần giữ layer của bản đồ)
folium.TileLayer('CartoDB Positron', name="CartoDB Positron").add_to(m)

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

# Thêm colormap
colormap.height = 35
colormap.width = 350
colormap.add_to(m)

# Cập nhật phạm vi hiển thị
m.fit_bounds([[miny, minx], [maxy, maxx]])

# Lưu bản đồ
m.save('heatmap/Hanoimap.html')
