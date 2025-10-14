# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## 📋 Chuẩn bị trước khi deploy

### 1. Cấu trúc thư mục cần có:
```
deploy/
├── WEBBpy.py           # File chính của ứng dụng
├── 210.csv             # Dữ liệu phim
├── sim_matrix.csv      # Ma trận độ tương đồng
├── requirements.txt    # Các thư viện cần thiết
└── README.md          # Tài liệu hướng dẫn
```

### 2. Kiểm tra file requirements.txt:
```txt
streamlit>=1.28.0
pandas>=2.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
```

## 🔧 Các bước deploy lên Streamlit Cloud

### Bước 1: Tạo Repository trên GitHub

1. Đăng nhập vào GitHub: https://github.com
2. Click **"New repository"** (nút màu xanh)
3. Đặt tên repo: `movie-recommendation-system` (hoặc tên bạn muốn)
4. Chọn **Public** (bắt buộc để deploy free)
5. Click **"Create repository"**

### Bước 2: Upload code lên GitHub

#### Cách 1: Sử dụng GitHub Desktop (Dễ nhất)
1. Tải và cài đặt GitHub Desktop: https://desktop.github.com
2. Mở GitHub Desktop, đăng nhập tài khoản
3. Click **"Clone a repository"**
4. Chọn repo vừa tạo
5. Copy tất cả file trong thư mục `deploy/` vào thư mục local của repo
6. Trong GitHub Desktop:
   - Viết commit message: "Initial commit"
   - Click **"Commit to main"**
   - Click **"Push origin"**

#### Cách 2: Sử dụng Git Command Line
```bash
cd D:\DaiHoc\BasicPython\Movie_Recommendation_system_project\deploy

# Khởi tạo git (nếu chưa có)
git init

# Thêm remote repository
git remote add origin https://github.com/YOUR_USERNAME/movie-recommendation-system.git

# Thêm tất cả file
git add .

# Commit
git commit -m "Initial commit"

# Push lên GitHub
git branch -M main
git push -u origin main
```

#### Cách 3: Upload trực tiếp trên Web (Nhanh nhất cho người mới)
1. Vào repo trên GitHub
2. Click **"Add file"** → **"Upload files"**
3. Kéo thả hoặc chọn tất cả file trong thư mục `deploy/`
4. Click **"Commit changes"**

### Bước 3: Deploy trên Streamlit Cloud

1. Truy cập: https://share.streamlit.io
2. Đăng nhập bằng tài khoản GitHub
3. Click **"New app"**
4. Điền thông tin:
   - **Repository**: Chọn repo `movie-recommendation-system`
   - **Branch**: `main`
   - **Main file path**: `WEBBpy.py`
5. Click **"Deploy!"**

### Bước 4: Đợi deploy hoàn tất

- Quá trình deploy mất khoảng 2-5 phút
- Streamlit sẽ tự động:
  - Cài đặt các thư viện từ `requirements.txt`
  - Chạy ứng dụng
  - Cấp cho bạn một URL public

## ✅ Kiểm tra sau khi deploy

1. **Kiểm tra file dữ liệu**: Sidebar sẽ hiển thị thông báo:
   - ✅ "Đã tải dữ liệu từ: 210.csv"
   - ✅ "Đã tải similarity matrix"

2. **Test các chức năng**:
   - Trang chủ hiển thị phim nổi bật
   - Gợi ý phim hoạt động bình thường
   - Phân cụm phim có biểu đồ

## 🐛 Xử lý lỗi thường gặp

### Lỗi 1: "Không tìm thấy file dữ liệu"
**Nguyên nhân**: File CSV không có trong repo

**Giải pháp**:
1. Kiểm tra file `210.csv` và `sim_matrix.csv` đã được upload lên GitHub chưa
2. Vào repo trên GitHub, kiểm tra file có trong danh sách không
3. Nếu thiếu, upload lại file:
   ```bash
   git add 210.csv sim_matrix.csv
   git commit -m "Add data files"
   git push
   ```
4. Streamlit Cloud sẽ tự động redeploy

### Lỗi 2: "ModuleNotFoundError"
**Nguyên nhân**: Thiếu thư viện trong requirements.txt

**Giải pháp**:
1. Mở file `requirements.txt`
2. Thêm thư viện bị thiếu, ví dụ:
   ```txt
   streamlit>=1.28.0
   pandas>=2.0.0
   scikit-learn>=1.3.0
   numpy>=1.24.0
   ```
3. Push lại lên GitHub:
   ```bash
   git add requirements.txt
   git commit -m "Update requirements"
   git push
   ```

### Lỗi 3: App không load dữ liệu
**Nguyên nhân**: Đường dẫn file không đúng

**Giải pháp**: Code đã được sửa để tự động tìm file ở nhiều vị trí:
- Cùng thư mục với `WEBBpy.py` ✅ (đúng cho Streamlit Cloud)
- Thư mục cha
- Đường dẫn tuyệt đối

### Lỗi 4: File CSV quá lớn (>100MB)
**Nguyên nhân**: GitHub giới hạn file 100MB

**Giải pháp**:
1. Nén file CSV hoặc giảm dữ liệu
2. Hoặc sử dụng Git LFS:
   ```bash
   git lfs install
   git lfs track "*.csv"
   git add .gitattributes
   git add 210.csv sim_matrix.csv
   git commit -m "Add large files with LFS"
   git push
   ```

## 🔄 Cập nhật ứng dụng sau khi deploy

Khi bạn sửa code hoặc dữ liệu:

1. Sửa file trên local
2. Push lên GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```
3. Streamlit Cloud tự động detect và redeploy (1-2 phút)

Hoặc force reboot:
- Vào Streamlit Cloud dashboard
- Click vào app
- Click **"Reboot app"**

## 📊 Giám sát ứng dụng

### Xem logs:
1. Vào Streamlit Cloud dashboard
2. Click vào app của bạn
3. Click **"Manage app"** → **"Logs"**
4. Xem lỗi nếu có

### Xem thống kê:
- Số lượng người truy cập
- Thời gian sử dụng
- Lỗi runtime

## 🎯 Tips để app chạy mượt

1. **Sử dụng @st.cache_data**: Đã được implement để cache dữ liệu
2. **Giới hạn dữ liệu**: Không nên quá nhiều phim (>1000)
3. **Tối ưu ảnh**: Nếu có ảnh, nén trước khi upload
4. **Monitor memory**: Streamlit Cloud free có giới hạn RAM

## 🆓 Giới hạn Streamlit Cloud Free

- **1 private app** hoặc **unlimited public apps**
- **1 GB RAM**
- **1 CPU core**
- **Unlimited bandwidth**

Đủ cho ứng dụng của bạn! 🎉

## 📞 Hỗ trợ thêm

Nếu gặp lỗi khác:
1. Check logs trên Streamlit Cloud
2. Kiểm tra file có đầy đủ trên GitHub
3. Xem lại requirements.txt
4. Restart app

## 🔗 Links hữu ích

- Streamlit Documentation: https://docs.streamlit.io
- Streamlit Cloud: https://share.streamlit.io
- GitHub: https://github.com
- Git Tutorial: https://git-scm.com/docs

