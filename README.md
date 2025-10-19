# 🚀 Tổng quan

Dự án này phân tích và dự đoán giá nhà tại **Hà Nội**.  
Dữ liệu được cào từ website **Batdongsan.com.vn** thông qua thư viện **Selenium**.

- **Frontend:** Bootstrap — deploy trên **Vercel**  
- **Backend:** API Flask dự đoán giá nhà — deploy trên **Render**  
- **Thuật toán mô hình:** Random Forest Regressor  
- **Các đặc trưng sử dụng:** `gia`, `dienTich`, `giaMoiM2`, `soPhongNgu`, `soWC`, `phuong`, `quan`

---

## 📁 Cấu trúc thư mục
```
house_price_analysis_and_prediction/
│
├── api/
│ └── api_model.py # Flask app (API chính)
│
├── model/
│ ├── house_price_model.pkl # File mô hình đã huấn luyện
│ └── train_model.py # Tiền xử lý và huấn luyện mô hình
│
├── data/ # Dữ liệu đã xử lý phục vụ cho việc phân tích
│
├── frontend/ # Giao diện người dùng
│
├── script/ # Script cào dữ liệu
│
├── data_cleaning/ # Script xử lý dữ liệu sau khi cào
│
├── README.md
└── requirements.txt
```

