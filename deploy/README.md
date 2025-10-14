# 🎬 Hệ Thống Gợi Ý Phim Việt Nam

Ứng dụng web gợi ý phim Việt Nam sử dụng Machine Learning với 2 phương pháp:
- **Similarity Matrix**: Dựa trên độ tương đồng nội dung (Cosine Similarity)
- **Clustering**: Phân cụm phim theo chủ đề (K-Means)

## 🚀 Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## 📦 Cấu trúc dữ liệu

Đảm bảo các file dữ liệu sau tồn tại:
- `../films_vn_with_content.csv`: File chứa thông tin phim
- `../sim_matrix.csv`: Ma trận độ tương đồng (tùy chọn, nếu không có sẽ tự tính)

## 🎯 Chạy ứng dụng

Từ thư mục deploy, chạy lệnh:
```bash
streamlit run WEBBpy.py
```

Hoặc nếu bạn ở thư mục khác:
```bash
cd Movie_Recommendation_system_project/deploy
streamlit run WEBBpy.py
```

## 📋 Tính năng

### 1. 🏠 Trang chủ
- Giới thiệu hệ thống
- Hiển thị các phim nổi bật

### 2. 🎯 Gợi ý phim
- **2 phương pháp gợi ý:**
  - **Similarity Matrix**: Tìm phim có nội dung tương tự dựa trên độ tương đồng cosine
  - **Clustering**: Tìm phim cùng cụm (cùng chủ đề)
- **2 cách tìm kiếm phim:**
  - **📋 Chọn từ danh sách**: Dropdown với tất cả tên phim có sẵn
  - **✍️ Tìm kiếm tự do**: 
    - Gõ một phần tên phim (VD: "Mai", "Bố", "Nhà")
    - Hệ thống tự động gợi ý các phim phù hợp ngay khi bạn gõ
    - Hiển thị danh sách phim khớp để chọn nhanh
    - Không cần gõ hết tên phim
- Nhập tên phim và nhận gợi ý top 10 phim tương tự
- Hiển thị độ tương đồng hoặc cụm phim

### 3. ⭐ Phim hay
- Danh sách các phim đề xuất
- Sắp xếp theo doanh thu (nếu có)

### 4. 📊 Phân cụm phim
- Thống kê số lượng phim theo từng cụm
- Xem danh sách phim trong mỗi cụm
- Biểu đồ trực quan

## 🛠️ Công nghệ sử dụng

- **Streamlit**: Framework web
- **Pandas**: Xử lý dữ liệu
- **Scikit-learn**: Machine Learning (TF-IDF, K-Means, Cosine Similarity)
- **NumPy**: Tính toán ma trận

## 📝 Cột dữ liệu cần thiết

File CSV cần có các cột (một trong các tên sau):
- Tên phim: `Phim` hoặc `Tên Phim` hoặc `title`
- Nội dung: `Content` hoặc `Nội dung`
- Năm: `Năm` hoặc `year`
- Đạo diễn: `Đạo diễn` hoặc `director`
- Doanh thu (tùy chọn): `Doanh thu (tỷ VNĐ)`

## 🎨 Giao diện

- Theme tối với màu chủ đạo đỏ Netflix
- Responsive design
- Hiệu ứng hover và animation
- Layout rõ ràng, dễ sử dụng
- **Autocomplete thông minh** khi tìm kiếm phim

## ✨ Điểm nổi bật mới

### 🔍 Tính năng Autocomplete/Gợi ý thông minh:
1. **Chọn từ danh sách**: Dropdown hiển thị tất cả phim, có thể cuộn hoặc gõ để tìm
2. **Tìm kiếm tự do**: 
   - Gõ một phần tên phim (không phân biệt hoa thường)
   - Hiển thị ngay các phim khớp
   - Nếu ≤10 phim: Hiển thị radio buttons để chọn nhanh
   - Nếu >10 phim: Hiển thị danh sách và gợi ý nhập thêm ký tự
   - Hỗ trợ tìm kiếm tiếng Việt có dấu

**Ví dụ sử dụng:**
- Gõ "Mai" → Tìm thấy phim "Mai"
- Gõ "Bố" → Tìm thấy "Bố già"
- Gõ "Lật" → Tìm thấy "Lật mặt 7: Một điều ước", "Lật mặt 6: Tấm vé định mệnh"
- Gõ "Nhà bà" → Tìm thấy "Nhà bà Nữ"

## 📞 Hỗ trợ

Nếu gặp lỗi, kiểm tra:
1. Đường dẫn file CSV có đúng không
2. Các thư viện đã cài đặt đầy đủ chưa
3. File CSV có đủ cột dữ liệu cần thiết không
