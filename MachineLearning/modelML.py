import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

# Bước 1: Đọc dữ liệu
data = pd.read_csv("../DataProcessing/cleaned_data.csv")

# Kiểm tra dữ liệu có bị rỗng không và loại bỏ các dòng rỗng (nếu cần)
data = data.dropna()

# Bước 2: Chọn đặc trưng (features) và biến mục tiêu (target)
X = data[['Xã/Phường', 'Quận/Huyện', 'Chủ đầu tư', 'Tên dự án', 'Diện tích', 'Số phòng ngủ', 'Số toilet', 'Pháp lý', 'Nội thất', 'Mặt tiền', 'Hướng nhà']]
y = data['Mức giá']

# Bước 3: Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Bước 4: Định nghĩa các cột phân loại và số để xử lý
categorical_features = ['Xã/Phường', 'Quận/Huyện', 'Chủ đầu tư', 'Tên dự án', 'Pháp lý', 'Nội thất', 'Hướng nhà']
numerical_features = ['Diện tích', 'Số phòng ngủ', 'Số toilet', 'Mặt tiền']

# Bước 5: Tạo các bước xử lý dữ liệu trong pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# Bước 6: Xây dựng pipeline cho mô hình với XGBRegressor
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42))
])

# Bước 7: Huấn luyện mô hình
model.fit(X_train, y_train)

# Bước 8: Dự đoán giá trên tập kiểm tra
y_pred = model.predict(X_test)

# Bước 9: Tính toán độ chính xác của mô hình (MAE và RMSE)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)

print("Mean Absolute Error (MAE):", mae)
print("Root Mean Squared Error (RMSE):", rmse)

# Bước 10: Lưu mô hình đã huấn luyện (nếu cần thiết)
joblib.dump(model, 'real_estate_price_predictor.pkl')
