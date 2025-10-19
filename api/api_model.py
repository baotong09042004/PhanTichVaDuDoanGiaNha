from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
import logging


app = Flask(__name__)
CORS(app)  

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "../model/house_price_model.pkl"
)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Không tìm thấy model tại: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
logging.info(f"Đã load model thành công từ: {MODEL_PATH}")

# Các cột đặc trưng yêu cầu từ frontend
REQUIRED_FEATURES = ["phuong", "quan", "dienTich", "soPhongNgu", "soWC"]


@app.route("/")
@app.route("/health")
def health_check():
    """API kiểm tra tình trạng server (dùng để keep-alive)"""
    return jsonify({
        "status": "OK",
    }), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        logging.info(f"Dữ liệu nhận được: {data}")

        # Kiểm tra đầu vào
        if not data:
            return jsonify({"error": "Không nhận được dữ liệu JSON"}), 400

        missing_features = [f for f in REQUIRED_FEATURES if f not in data]
        if missing_features:
            return jsonify({"error": f"Thiếu các thuộc tính: {', '.join(missing_features)}"}), 400

        df = pd.DataFrame([data])

        # Thực hiện dự đoán
        prediction = model.predict(df)

        # Kiểm tra định dạng đầu ra
        if prediction.ndim == 1 or len(prediction[0]) == 1:
            response = {"gia": float(prediction[0])}
        else:
            response = {
                "gia": float(prediction[0][0]),
                "giaMoiM2": float(prediction[0][1])
            }

        logging.info(f"Kết quả dự đoán: {response}")
        return jsonify(response)

    except Exception as e:
        logging.error(f"Lỗi trong quá trình dự đoán: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
