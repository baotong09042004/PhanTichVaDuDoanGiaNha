import pandas as pd
import re
import os

file_path = os.path.join(os.path.dirname(__file__), "../data/batdongsan_data.csv")
df = pd.read_csv(file_path)

# Hàm chuyển đổi số: thay dấu ',' bằng '.' rồi chuyển thành float
def convert_to_number(value):
    if isinstance(value, str):
        value = value.replace(",", ".")  # Thay dấu , thành .
        value = re.sub(r"[^\d.]", "", value)  # Loại bỏ ký tự không phải số
        return float(value) if value else None
    return value

# Chuyển đổi dữ liệu các cột số
df["gia"] = df["gia"].apply(convert_to_number)
df["dienTich"] = df["dienTich"].apply(convert_to_number)
df["giaMoiM2"] = df["giaMoiM2"].apply(convert_to_number)
df["soPhongNgu"] = pd.to_numeric(df["soPhongNgu"], errors="coerce")
df["soWC"] = pd.to_numeric(df["soWC"], errors="coerce")

# Chắc chắn "Phường" và "Quận" là dạng chuỗi
df["phuong"] = df["phuong"].astype(str)
df["quan"] = df["quan"].astype(str)

# Lưu lại file CSV
df.to_csv(file_path, index=False, encoding="utf-8-sig")

print("Dữ liệu đã được làm sạch và cập nhật!")
