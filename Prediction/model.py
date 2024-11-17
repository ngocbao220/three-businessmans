import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import numpy as np

class PricePredictor:
    def __init__(self, model=None):
        # Xác định các cột phân loại và số
        self.categorical_features = ['Xã/Phường', 'Quận/Huyện', 'Chủ đầu tư', 'Tên dự án', 'Pháp lý', 'Nội thất']
        self.numerical_features = ['Diện tích (m²)', 'Số phòng ngủ (phòng)', 'Số toilet (phòng)']

        # Tiền xử lý dữ liệu: Impute và chuẩn hóa
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='mean')),  # Xử lý giá trị thiếu cho đặc trưng số
                    ('scaler', StandardScaler())  # Chuẩn hóa các đặc trưng số
                ]), self.numerical_features),
                ('cat', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute giá trị thiếu cho đặc trưng phân loại
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))  # OneHotEncoder cho các đặc trưng phân loại
                ]), self.categorical_features)
            ])

        # Lưu trữ giá trị phổ biến cho các cột phân loại (tránh việc đọc lại mỗi lần)
        self.most_frequent_values = {}
        for feature in self.categorical_features:
            self.most_frequent_values[feature] = self._get_most_frequent_value(feature)

        # Nếu không có mô hình, huấn luyện mô hình mặc định
        if model is None:
            self.model = self._train_default_model()
        else:
            self.model = model

    def _train_default_model(self):
        """
        Huấn luyện mô hình XGBoost mặc định.
        """
        # Đọc dữ liệu
        data = pd.read_csv('../Data/standardizedData/standardized_data.csv')
        X = data.drop(['Mức giá (triệu/m²)', 'Mã lịch sử giá'], axis=1)
        y = data['Mức giá (triệu/m²)']
        
        # Chia dữ liệu
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Tạo pipeline và huấn luyện mô hình
        model = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('regressor', xgb.XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror'))
        ])
        
        model.fit(X_train, y_train)
        
        # Đánh giá mô hình
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f'Mean Absolute Error: {mae}')
        
        return model

    def get_price(self, **kwargs):
        """
        Dự đoán giá của căn nhà khi nhận các tham số từ người dùng.
        Nếu thiếu tham số, mô hình sẽ tự động dự đoán.
        
        Args:
        **kwargs: các tham số đặc trưng của căn nhà, ví dụ: Diện tích, số phòng, quận, pháp lý, ...
        
        Returns:
        giá dự đoán và sai số (hoặc xác suất đúng)
        """
        # Tạo dataframe từ các tham số đầu vào
        input_data = pd.DataFrame([kwargs])

        # Kiểm tra các tham số thiếu và xử lý tự động
        missing_columns = list(set(self.categorical_features + self.numerical_features) - set(kwargs.keys()))
        for column in missing_columns:
            if column in self.categorical_features:
                input_data[column] = [self.most_frequent_values[column]]
            else:
                input_data[column] = [np.mean(self.model.named_steps['preprocessor'].transformers_[0][1].steps[0][1].statistics_)]

        # Tiền xử lý đầu vào
        processed_data = self.preprocessor.fit_transform(input_data)  # Sử dụng fit_transform thay vì transform
        
        # Dự đoán giá trị
        predicted_price = self.model.predict(processed_data)
        
        # Tính sai số dự đoán (mean absolute error so với tập huấn luyện)
        mae = np.abs(predicted_price - np.mean(self.model.predict(self.preprocessor.transform(input_data))))
        
        return predicted_price[0], mae

    def _get_most_frequent_value(self, column):
        """
        Trả về giá trị xuất hiện nhiều nhất trong cột phân loại.
        """
        data = pd.read_csv('../Data/standardizedData/standardized_data.csv')
        return data[column].mode()[0]
    
# Khởi tạo mô hình dự đoán
predictor = PricePredictor()

# Dữ liệu của căn nhà mà bạn muốn dự đoán giá
input_data = {
    'Xã/Phường': 'Dương Xá',
    'Quận/Huyện': 'Gia Lâm',
    'Chủ đầu tư': 'Tập đoàn Vingroup',
    'Tên dự án': 'Vinhomes Ocean Park Gia Lâm',
    'Diện tích (m²)': 55.0,
    'Số phòng ngủ (phòng)': 2.0,
    'Số toilet (phòng)': 1.0,
    'Pháp lý': 'Đầy đủ',
    'Nội thất': 'Cơ bản'
}

# Dự đoán giá của căn nhà
price, mae = predictor.get_price(**input_data)

# In kết quả
print(f'Giá dự đoán: {price} triệu/m², Sai số dự đoán: {mae} triệu/m²')
