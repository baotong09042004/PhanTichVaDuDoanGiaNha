import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os



def load_data(csv_path: str) -> pd.DataFrame:
    """Đọc dữ liệu từ file CSV."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Không tìm thấy file CSV tại: {csv_path}")

    try:
        data = pd.read_csv(csv_path)
        print(f"Đã tải {data.shape[0]} dòng, {data.shape[1]} cột từ {csv_path}")
        return data
    except Exception as e:
        raise RuntimeError(f"Lỗi khi đọc CSV: {e}")



def split_data(data: pd.DataFrame):
    """chia dữ liệu train/test."""
    X = data.drop(columns=['gia', 'giaMoiM2'])
    y = data[['gia', 'giaMoiM2']]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test



def build_pipeline():
    """Tạo pipeline gồm tiền xử lý và mô hình RandomForest."""
    categorical_features = ['phuong', 'quan']
    numeric_features = ['dienTich', 'soPhongNgu', 'soWC']

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ])

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])

    return pipeline



def train_and_evaluate(pipeline, X_train, X_test, y_train, y_test, param_grid, model_path):
    """Huấn luyện mô hình, tối ưu siêu tham số, đánh giá và lưu model."""
    print("Đang huấn luyện mô hình (GridSearchCV)...")
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=3,
        scoring='neg_mean_absolute_error',
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print("Cấu hình tốt nhất tìm được:")
    print(grid_search.best_params_)

    y_pred = best_model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.3f}")
    print(f"R²: {r2_score(y_test, y_pred):.3f}")

    
    best_model.fit(pd.concat([X_train, X_test]), pd.concat([y_train, y_test]))

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(best_model, model_path)
    print(f"Mô hình đã được lưu tại: {model_path}")



def train_optimized_model():
    """Huấn luyện mô hình với tối ưu siêu tham số sử dụng GridSearchCV."""
    csv_path = os.path.join(os.path.dirname(__file__), "../data/batdongsan_data.csv")
    model_path = os.path.join(os.path.dirname(__file__), "house_price_model.pkl")

    data = load_data(csv_path)
    X_train, X_test, y_train, y_test = split_data(data)
    pipeline = build_pipeline()

    # Lưới tham số
    param_grid = {
        'regressor__n_estimators': [100, 200],
        'regressor__max_depth': [None, 10, 20],
        'regressor__min_samples_split': [2, 5],
        'regressor__min_samples_leaf': [1, 2],
        'regressor__max_features': ['sqrt', 'log2', None]
    }

    train_and_evaluate(pipeline, X_train, X_test, y_train, y_test, param_grid, model_path)


if __name__ == "__main__":
    train_optimized_model()
