from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from DataProcessing.StandardizeData import Price
import pandas as pd

data = pd.read_csv('Data/standardizedData/standardized_data.csv')

# Predict price of non_exist building
X = data.drop(['Mức giá (triệu/m²)', 'Mã lịch sử giá'], axis=1)
y = data['Mức giá (triệu/m²)']

categorical_features = ['Xã/Phường', 'Quận/Huyện', 'Chủ đầu tư', 'Tên dự án', 'Pháp lý', 'Nội thất']
numerical_features = ['Diện tích (m²)', 'Số phòng ngủ (phòng)', 'Số toilet (phòng)']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor())
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Predict price of trend in the future
