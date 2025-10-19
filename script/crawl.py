import pandas as pd
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Khởi tạo trình duyệt Edge
options = webdriver.EdgeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)   

# Danh sách URL cần crawl
urls = [f"https://batdongsan.com.vn/ban-can-ho-chung-cu-long-bien/p{i}?sortValue=1&tpl=list&gtn=1-ty&gcn=25-ty" for i in range(1, 30)]

# Lưu dữ liệu
data = []

for url in urls:
    print(f"Crawling {url} ...")
    driver.get(url)
    
    # Đợi trang tải xong
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "re__card-info-content")))

    # Lấy danh sách tin đăng
    listings = driver.find_elements(By.CLASS_NAME, "re__card-info-content")
    
    for listing in listings:
        try:
            price = listing.find_element(By.CLASS_NAME, "re__card-config-price").text.strip()
        except:
            price = "Không có dữ liệu"

        try:
            area = listing.find_element(By.CLASS_NAME, "re__card-config-area").text.strip()
        except:
            area = "Không có dữ liệu"

        try:
            price_per_m2 = listing.find_element(By.CLASS_NAME, "re__card-config-price_per_m2").text.strip()
        except:
            price_per_m2 = "Không có dữ liệu"

        try:
            bedrooms = listing.find_element(By.CLASS_NAME, "re__card-config-bedroom").find_element(By.TAG_NAME, "span").text.strip()
        except:
            bedrooms = "Không có dữ liệu"

        try:
            bathrooms = listing.find_element(By.CLASS_NAME, "re__card-config-toilet").find_element(By.TAG_NAME, "span").text.strip()
        except:
            bathrooms = "Không có dữ liệu"

        try:
            location = listing.find_element(By.CLASS_NAME, "re__card-location").find_element(By.TAG_NAME, "span").text.strip()
        except:
            location = "Không có dữ liệu"

        # Tách "Phường" và "Quận" từ "Vị trí"
        location_parts = location.split(", ")
        if len(location_parts) == 2:
            ward, district = location_parts
        else:
            ward, district = "Không có dữ liệu", "Không có dữ liệu"

        # Lưu vào danh sách
        data.append([price, area, price_per_m2, bedrooms, bathrooms, ward, district])

# Đóng trình duyệt
driver.quit()

# Chuyển dữ liệu thành DataFrame
file_path = "Housepriceprediction/batdongsan_data.csv"
write_header = not os.path.exists(file_path)

df = pd.DataFrame(data, columns=["gia", "dienTich", "giaMoiM2", "soPhongNgu", "soWC", "phuong", "quan"])
df.to_csv(file_path, mode='a', header=write_header, index=False, encoding="utf-8-sig")

print("Dữ liệu đã được làm sạch và cập nhật.")
