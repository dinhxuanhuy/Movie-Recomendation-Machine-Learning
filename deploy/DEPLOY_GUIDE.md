# 🚀 Hướng dẫn Deploy lên Streamlit Cloud

## 📋 Chuẩn bị trước khi deploy

### 1. Cấu trúc thư mục cần có (QUAN TRỌNG):
```
deploy/
├── WEBBpy.py           # File chính của ứng dụng
├── 210.csv             # Dữ liệu 210 phim (BẮT BUỘC - có cột 'cluster')
├── sim_matrix.csv      # Ma trận độ tương đồng (BẮT BUỘC)
├── requirements.txt    # Các thư viện cần thiết
└── README.md          # Tài liệu hướng dẫn
```

**⚠️ LƯU Ý QUAN TRỌNG:**
- File `210.csv` PHẢI có cột `cluster` (giá trị 0-6) để chức năng **Phân cụm** hoạt động
- File `sim_matrix.csv` PHẢI có để chức năng **Similarity Matrix** hoạt động
- Cả 3 file (WEBBpy.py, 210.csv, sim_matrix.csv) phải cùng nằm trong 1 thư mục

### 2. Kiểm tra file 210.csv:
```python
import pandas as pd
df = pd.read_csv('210.csv')
print(df.columns)  # Phải có cột: 'Tên Phim', 'Năm', 'Đạo diễn', 'Nội dung', 'cluster'
print(df['cluster'].unique())  # Phải có các giá trị: [0, 1, 2, 3, 4, 5, 6]
```

### 3. Kiểm tra file requirements.txt:
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

### Lỗi 1: "Không tìm thấy file dữ liệu" hoặc "Không có dữ liệu phân cụm"
**Nguyên nhân**: File CSV không có trong repo hoặc sai cấu trúc thư mục

**Giải pháp**:

1. **Kiểm tra cấu trúc thư mục trên GitHub:**
   - Vào repo trên GitHub
   - Đảm bảo có 3 file cùng cấp: `WEBBpy.py`, `210.csv`, `sim_matrix.csv`
   - **KHÔNG** đặt file CSV trong thư mục con
   
2. **Kiểm tra file 210.csv có cột cluster:**
   ```python
   # Mở file 210.csv, kiểm tra có cột 'cluster' không
   import pandas as pd
   df = pd.read_csv('210.csv')
   print(df.columns)  # Phải thấy 'cluster' trong danh sách
   print(df['cluster'].value_counts())  # Phải có các giá trị 0-6
   ```

3. **Nếu thiếu file, upload lại:**
   ```bash
   cd D:\DaiHoc\BasicPython\Movie_Recommendation_system_project\deploy
   
   # Kiểm tra file có đúng chưa
   dir
   
   # Push lại lên GitHub
   git add 210.csv sim_matrix.csv WEBBpy.py
   git commit -m "Add data files with cluster column"
   git push
   ```

4. **Trên Streamlit Cloud:**
   - Vào App Settings → Reboot app
   - Kiểm tra Logs xem có thông báo "✅ Đã tải dữ liệu từ: 210.csv" không
   - Kiểm tra có thông báo "✅ Có dữ liệu phân cụm: 7 cụm" không

5. **Nếu vẫn lỗi, kiểm tra đường dẫn:**
   - Trong Streamlit Cloud logs, tìm dòng "📂 Đường dẫn:"
   - Tìm dòng "📋 Danh sách file trong thư mục:"
   - Xem file `210.csv` có trong danh sách không

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

### Lỗi 3: App không load dữ liệu hoặc "Không có cột cluster"
**Nguyên nhân**: Đường dẫn file không đúng hoặc file CSV thiếu cột

**Giải pháp**:

1. **Code đã được cải thiện** để tự động tìm file ở nhiều vị trí:
   - `os.path.join(current_dir, '210.csv')` ✅ (ƯU TIÊN - cho Streamlit Cloud)
   - `210.csv` ✅ (Relative path)
   - `os.getcwd() + '/210.csv'` ✅ (Current working directory)
   - Các fallback khác

2. **Kiểm tra sidebar trên Streamlit Cloud:**
   - Phải thấy: "✅ Đã tải dữ liệu từ: 210.csv"
   - Phải thấy: "✅ Có dữ liệu phân cụm: 7 cụm"
   - Phải thấy: "✅ Đã tải similarity matrix từ file"

3. **Nếu thiếu cột cluster:**
   - Mở file `210.csv` bằng Excel/Python
   - Đảm bảo có cột tên `cluster` (chữ thường)
   - Giá trị phải là số nguyên từ 0-6
   - Save lại và push lên GitHub

4. **Debug mode:**
   - App sẽ tự động hiển thị thông tin debug trong sidebar
   - Xem "📂 Đường dẫn" để biết file được load từ đâu
   - Xem "📋 Danh sách file" để biết file nào có sẵn

5. **Force reload:**
   ```bash
   # Local test trước
   cd D:\DaiHoc\BasicPython\Movie_Recommendation_system_project\deploy
   streamlit run WEBBpy.py
   
   # Nếu OK, push lên
   git add .
   git commit -m "Fix file paths for Streamlit Cloud"
   git push
   ```

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

