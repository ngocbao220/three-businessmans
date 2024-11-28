from shapely.geometry import shape
import json

# Đọc GeoJSON
with open('hanoi_boundary.geojson', 'r') as f:
    geojson = json.load(f)

# Lấy hình dạng đầu tiên (Hà Nội)
geometry = shape(geojson['features'][0]['geometry'])

# Chuyển đổi thành SVG Path
svg_path = geometry.svg(scale_factor=1000)
print(svg_path)
