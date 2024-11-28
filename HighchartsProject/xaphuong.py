import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
import branca.colormap as cm

# Đọc dữ liệu bất động sản từ file CSV
data = pd.read_csv('../Data/cleanedData/cleaned_data.csv')

# Loại bỏ các hàng có giá trị thiếu trong cột 'Xã/Phường' và 'Mức giá'
heatmap_data = data.dropna(subset=['Xã/Phường', 'Mức giá'])

# Chuyển đổi cột 'Mức giá' thành kiểu số
heatmap_data['Mức giá'] = pd.to_numeric(heatmap_data['Mức giá'], errors='coerce')

# Tính giá trung bình theo xã/phường
avg_price_by_ward = heatmap_data.groupby('Xã/Phường')['Mức giá'].mean().reset_index()

# Đọc shapefile của Việt Nam
vietnam_map = gpd.read_file('../VisualizationData/Map/commune map')
minx, miny, maxx, maxy = vietnam_map.total_bounds

def create_district_map(district_name):
    """
    Tạo bản đồ nhiệt cho quận/huyện được chọn, với zoom phù hợp dựa trên diện tích.
    """
    # Lọc bản đồ cho quận/huyện được chọn
    district_map = vietnam_map[(vietnam_map['NAME_1'] == 'Hà Nội') & (vietnam_map['NAME_2'] == district_name)]
    
    if district_map.empty:
        print(f"Không tìm thấy dữ liệu cho quận/huyện: {district_name}")
        return None
    # Ghép dữ liệu giá trung bình vào bản đồ
    district_map = district_map.to_crs(epsg=4326)  # Chuyển lại về hệ tọa độ địa lý
    district_map = district_map.merge(avg_price_by_ward, left_on='NAME_3', right_on='Xã/Phường', how='left')

    # Tọa độ trung tâm của quận/huyện
    district_center = [district_map.geometry.centroid.y.mean(), district_map.geometry.centroid.x.mean()]
    minx, miny, maxx, maxy = district_map.total_bounds
    # Tạo bản đồ nền
    m_district = folium.Map(
        location=district_center,
        tiles="CartoDB Positron",  # Nền mờ
        max_bounds=True,
        dragging=True,  # Cho phép kéo bản đồ
        zoom_control=False,  # Bật nút thu phóng
        scrollWheelZoom=True  # Bật cuộn chuột để phóng to
    )

    m_district.fit_bounds([[miny, minx], [maxy, maxx]])

    # Tạo colormap
    

    # Chuyển đổi GeoDataFrame thành GeoJson và thêm vào bản đồ
    folium.GeoJson(
        district_map,
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties']['Mức giá']) if feature['properties']['Mức giá'] else 'lightblue',
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

    return m_district

# Lọc dữ liệu Hà Nội
hanoi_map = vietnam_map[vietnam_map['NAME_1'] == 'Hà Nội']

# Lấy danh sách các quận/huyện trong Hà Nội
district_names = hanoi_map['NAME_2'].unique()
map_output = create_district_map('Hoàn Kiếm')
map_output.save('heatmap/Thanh_Oai.html')
# Tạo và lưu bản đồ nhiệt cho từng quận/huyện



