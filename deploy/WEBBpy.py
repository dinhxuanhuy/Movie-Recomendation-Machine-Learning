import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Cấu hình trang
st.set_page_config(page_title="Hệ thống gợi ý phim", page_icon="🎬", layout="wide")

# Load dữ liệu
@st.cache_data
def load_data():
    try:
        # Đọc dữ liệu phim - cập nhật để đọc từ 210.csv
        try:
            df = pd.read_csv('210.csv')
            # Set index nếu có cột 'Thứ hạng' hoặc 'Thứ Hạng'
            if 'Thứ hạng' in df.columns:
                df.set_index('Thứ hạng', inplace=True)
            elif 'Thứ Hạng' in df.columns:
                df.set_index('Thứ Hạng', inplace=True)
        except:
            df = pd.read_csv('../films_vn_with_content.csv', index_col=0)

        # Đọc similarity matrix nếu có
        try:
            sim_matrix = pd.read_csv('sim_matrix.csv', index_col=0)
        except:
            sim_matrix = None

        return df, sim_matrix
    except:
        # Fallback nếu không tìm thấy file
        st.error("Không tìm thấy file dữ liệu. Vui lòng kiểm tra đường dẫn.")
        return None, None

df, sim_matrix = load_data()

if df is not None:
    # Chuẩn hóa dữ liệu
    df = df.copy()
    if 'Content' in df.columns:
        df['Content'] = df['Content'].fillna('')
        df = df[df['Content'].str.strip() != '']
        df['Content'] = df['Content'].str.replace(r'\s+', ' ', regex=True).str.lower().str.strip()

# Helper functions
def snippet(text, n=250):
    if not isinstance(text, str):
        return ''
    text = text.strip()
    if len(text) <= n:
        return text
    return text[:n].rstrip() + '...'

def get_field(row, candidates):
    """Lấy giá trị từ các cột có thể có"""
    for c in candidates:
        if c in row.index:
            val = row[c]
            if pd.notna(val) and str(val).strip() != '':
                return val
    return 'Không có'

# Tạo TF-IDF và clustering
@st.cache_resource
def create_models(df):
    if 'Content' not in df.columns or df['Content'].isna().all():
        return None, None, None

    # TF-IDF
    tfidf = TfidfVectorizer(max_df=0.8, min_df=0.1, ngram_range=(1, 3))
    tfidf_matrix = tfidf.fit_transform(df['Content'])

    # KMeans Clustering
    n_clusters = min(8, len(df) // 5)  # Động theo số lượng phim
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(tfidf_matrix)

    # Tạo similarity matrix nếu chưa có
    similarity_matrix = cosine_similarity(tfidf_matrix)

    return clusters, similarity_matrix, tfidf_matrix

if df is not None and 'Content' in df.columns:
    clusters, similarity_matrix_computed, tfidf_matrix = create_models(df)
    if clusters is not None:
        df['cluster'] = clusters
else:
    clusters = None
    similarity_matrix_computed = None

# CSS Styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
    color: #f1f1f1;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #16213e 0%, #0f3460 100%);
}
h1, h2, h3, h4, h5, h6, .stMarkdown p {
    color: #f5f5f5 !important;
    font-family: 'Segoe UI', sans-serif;
}
div.stButton > button {
    background: linear-gradient(90deg, #E50914 0%, #ff4545 100%);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    height: 45px;
    width: 100%;
    transition: all 0.3s;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #ff1a1a 0%, #ff6666 100%);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(229, 9, 20, 0.4);
}
.movie-card {
    background: linear-gradient(145deg, #1e1e1e, #2d2d2d);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    transition: transform 0.3s, box-shadow 0.3s;
}
.movie-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(229, 9, 20, 0.3);
}
.stRadio > label {
    color: #f5f5f5 !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("# 🎬 HỆ THỐNG GỢI Ý PHIM")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "📌 Menu điều hướng",
    ["🏠 Trang chủ", "🎯 Gợi ý phim", "⭐ Phim hay", "📊 Phân cụm phim"]
)

# Trang chủ
if menu == "🏠 Trang chủ":
    st.markdown("""
        <h1 style='text-align:center; color:#E50914; font-size: 48px;'>
            🎬 HỆ THỐNG GỢI Ý PHIM VIỆT NAM
        </h1>
        <p style='text-align:center; color:#aaa; font-size: 18px;'>
            Khám phá những bộ phim Việt Nam hay nhất với công nghệ AI
        </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style='text-align:center; padding: 20px; background: linear-gradient(145deg, #1e1e1e, #2d2d2d); border-radius: 15px;'>
                <h2>🎯</h2>
                <h3>Gợi ý thông minh</h3>
                <p>Sử dụng AI để gợi ý phim phù hợp với sở thích của bạn</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='text-align:center; padding: 20px; background: linear-gradient(145deg, #1e1e1e, #2d2d2d); border-radius: 15px;'>
                <h2>📊</h2>
                <h3>Phân cụm nội dung</h3>
                <p>Phân loại phim theo chủ đề và nội dung tương tự</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style='text-align:center; padding: 20px; background: linear-gradient(145deg, #1e1e1e, #2d2d2d); border-radius: 15px;'>
                <h2>🔍</h2>
                <h3>Tìm kiếm dễ dàng</h3>
                <p>Tìm phim nhanh chóng với hệ thống tìm kiếm thông minh</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    if df is not None:
        st.markdown("### 🎥 Một số bộ phim nổi bật")
        top_films = df.head(6) if 'Doanh thu (tỷ VNĐ)' not in df.columns else df.nlargest(6, 'Doanh thu (tỷ VNĐ)')

        cols = st.columns(3)
        for i, (idx, film) in enumerate(top_films.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class='movie-card'>
                        <h4 style='color: #E50914;'>{get_field(film, ['Phim', 'Tên Phim', 'title'])}</h4>
                        <p><strong>Năm:</strong> {get_field(film, ['Năm', 'year'])}</p>
                        <p><strong>Đạo diễn:</strong> {get_field(film, ['Đạo diễn', 'director'])}</p>
                    </div>
                """, unsafe_allow_html=True)

# Gợi ý phim
elif menu == "🎯 Gợi ý phim":
    st.markdown("<h1 style='text-align:center; color:#E50914;'>🎯 GỢI Ý PHIM THÔNG MINH</h1>", unsafe_allow_html=True)
    st.markdown("---")

    if df is None:
        st.error("Không thể tải dữ liệu phim!")
    else:
        # Chọn phương pháp gợi ý
        col1, col2 = st.columns(2)
        with col1:
            method = st.radio(
                "🔧 Chọn phương pháp gợi ý:",
                ["📊 Similarity Matrix (Độ tương đồng)", "🎯 Clustering (Phân cụm)"],
                help="Similarity Matrix: Dựa trên độ tương đồng nội dung\nClustering: Dựa trên nhóm phim có chủ đề giống nhau"
            )

        # Input tên phim với autocomplete
        st.markdown("### 🔍 Tìm phim để gợi ý")

        # Lấy danh sách tên phim
        movie_col = 'Phim' if 'Phim' in df.columns else 'Tên Phim'
        all_movies = df[movie_col].dropna().unique().tolist()
        all_movies = sorted([str(movie) for movie in all_movies])

        # Tạo 2 cột: Dropdown và Input tự do
        tab1, tab2 = st.tabs(["📋 Chọn từ danh sách", "✍️ Tìm kiếm tự do"])

        with tab1:
            st.markdown("#### Chọn phim từ danh sách có sẵn")
            selected_from_list = st.selectbox(
                "Chọn phim:",
                options=[""] + all_movies,
                format_func=lambda x: "-- Chọn một phim --" if x == "" else x,
                key="movie_selectbox"
            )
            search_button_list = st.button("🎬 Gợi ý từ danh sách", use_container_width=True, key="btn_list")
            movie_name = selected_from_list if search_button_list else ""
            search_button = search_button_list

        with tab2:
            st.markdown("#### Tìm kiếm phim theo tên (hỗ trợ tìm kiếm một phần)")
            col1, col2 = st.columns([4, 1])
            with col1:
                search_text = st.text_input(
                    "Nhập tên phim hoặc một phần tên phim:",
                    placeholder="Ví dụ: Mai, Bố, Nhà bà...",
                    label_visibility="collapsed",
                    key="movie_search"
                )
            with col2:
                search_button_free = st.button("🎬 Tìm kiếm", use_container_width=True, key="btn_free")

            # Hiển thị gợi ý khi người dùng đang gõ
            if search_text.strip():
                matching_movies = [m for m in all_movies if search_text.lower() in m.lower()]
                if matching_movies:
                    st.info(f"🔍 Tìm thấy {len(matching_movies)} phim phù hợp")

                    # Hiển thị tối đa 10 phim gợi ý
                    if len(matching_movies) <= 10:
                        st.markdown("**Các phim phù hợp:**")
                        selected_suggestion = st.radio(
                            "Chọn phim:",
                            options=matching_movies,
                            key="suggestions",
                            label_visibility="collapsed"
                        )
                        if st.button("✅ Chọn phim này", key="btn_suggestion"):
                            movie_name = selected_suggestion
                            search_button = True
                    else:
                        st.markdown(f"**{len(matching_movies)} phim được tìm thấy** (Hiển thị 15 phim đầu tiên):")
                        cols = st.columns(3)
                        for i, movie in enumerate(matching_movies[:15]):
                            with cols[i % 3]:
                                st.markdown(f"• {movie}")
                        st.info("💡 Nhập thêm ký tự để thu hẹp kết quả tìm kiếm")
                else:
                    st.warning("❌ Không tìm thấy phim nào phù hợp")

            if search_button_free and search_text.strip():
                # Tìm phim khớp nhất
                matching_movies = [m for m in all_movies if search_text.lower() in m.lower()]
                if matching_movies:
                    movie_name = matching_movies[0]  # Chọn phim đầu tiên khớp nhất
                    search_button = True
                else:
                    movie_name = search_text
                    search_button = True

        if search_button and movie_name and movie_name.strip():
            # Tìm phim
            movie_match = df[df[movie_col].str.lower().str.contains(movie_name.lower(), na=False)]

            if movie_match.empty:
                st.error(f"❌ Không tìm thấy phim '{movie_name}'")
                st.info("💡 Gợi ý: Thử tìm kiếm với từ khóa khác hoặc viết tắt tên phim")
            else:
                # Hiển thị phim được tìm thấy
                selected_movie = movie_match.iloc[0]
                selected_idx = movie_match.index[0]

                st.success(f"✅ Đã tìm thấy phim: **{get_field(selected_movie, ['Phim', 'Tên Phim', 'title'])}**")

                with st.expander("📖 Thông tin phim đã chọn", expanded=True):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**🎬 Tên phim:** {get_field(selected_movie, ['Phim', 'Tên Phim', 'title'])}")
                        st.markdown(f"**📅 Năm:** {get_field(selected_movie, ['Năm', 'year'])}")
                        st.markdown(f"**🎭 Đạo diễn:** {get_field(selected_movie, ['Đạo diễn', 'director'])}")
                        if 'Doanh thu (tỷ VNĐ)' in selected_movie.index:
                            st.markdown(f"**💰 Doanh thu:** {get_field(selected_movie, ['Doanh thu (tỷ VNĐ)'])} tỷ VNĐ")
                    with col2:
                        content = get_field(selected_movie, ['Content', 'Nội dung'])
                        st.markdown("**📝 Nội dung:**")
                        st.write(snippet(content, 300))

                st.markdown("---")

                # Gợi ý theo phương pháp được chọn
                if "Similarity Matrix" in method:
                    st.markdown("### 🎯 Các phim tương tự (dựa trên Similarity Matrix)")

                    if sim_matrix is not None and not sim_matrix.empty:
                        # Sử dụng similarity matrix đã có
                        movie_title = get_field(selected_movie, ['Phim', 'Tên Phim', 'title'])
                        if movie_title in sim_matrix.columns:
                            similarities = sim_matrix[movie_title].sort_values()
                            similar_movies = similarities[1:6]  # Top 5, bỏ chính nó

                            for i, (movie, score) in enumerate(similar_movies.items(), 1):
                                similar_film = df[df[movie_col] == movie]
                                if not similar_film.empty:
                                    similar_film = similar_film.iloc[0]
                                    similarity_percent = (1 - score) * 100

                                    with st.container():
                                        st.markdown(f"""
                                            <div class='movie-card'>
                                                <h4 style='color: #E50914;'>{i}. {movie}</h4>
                                                <p><strong>📊 Độ tương đồng:</strong> {similarity_percent:.1f}%</p>
                                                <p><strong>📅 Năm:</strong> {get_field(similar_film, ['Năm', 'year'])}</p>
                                                <p><strong>🎭 Đạo diễn:</strong> {get_field(similar_film, ['Đạo diễn', 'director'])}</p>
                                            </div>
                                        """, unsafe_allow_html=True)

                                        content = get_field(similar_film, ['Content', 'Nội dung'])
                                        st.write(snippet(content, 200))
                                        if isinstance(content, str) and content.strip():
                                            with st.expander("📖 Đọc thêm"):
                                                st.write(content)
                                        st.markdown("---")
                        else:
                            st.warning("Không tìm thấy thông tin similarity cho phim này trong ma trận")

                    elif similarity_matrix_computed is not None:
                        # Sử dụng similarity matrix vừa tính
                        similarities = similarity_matrix_computed[selected_idx]
                        similar_indices = np.argsort(similarities)[::-1][1:6]  # Top 5, bỏ chính nó

                        for i, idx in enumerate(similar_indices, 1):
                            similar_film = df.iloc[idx]
                            similarity_percent = similarities[idx] * 100

                            with st.container():
                                st.markdown(f"""
                                    <div class='movie-card'>
                                        <h4 style='color: #E50914;'>{i}. {get_field(similar_film, ['Phim', 'Tên Phim', 'title'])}</h4>
                                        <p><strong>📊 Độ tương đồng:</strong> {similarity_percent:.1f}%</p>
                                        <p><strong>📅 Năm:</strong> {get_field(similar_film, ['Năm', 'year'])}</p>
                                        <p><strong>🎭 Đạo diễn:</strong> {get_field(similar_film, ['Đạo diễn', 'director'])}</p>
                                    </div>
                                """, unsafe_allow_html=True)

                                content = get_field(similar_film, ['Content', 'Nội dung'])
                                st.write(snippet(content, 200))
                                if isinstance(content, str) and content.strip():
                                    with st.expander("📖 Đọc thêm"):
                                        st.write(content)
                                st.markdown("---")
                    else:
                        st.error("Không có dữ liệu similarity matrix")

                else:  # Clustering
                    st.markdown("### 🎯 Các phim cùng cụm (dựa trên Clustering)")

                    if 'cluster' in df.columns:
                        cluster_value = selected_movie['cluster']
                        same_cluster_films = df[df['cluster'] == cluster_value]
                        same_cluster_films = same_cluster_films[same_cluster_films.index != selected_idx]

                        st.info(f"🎯 Cụm #{cluster_value} có {len(same_cluster_films)} phim tương tự")

                        for i, (idx, film) in enumerate(same_cluster_films.head(10).iterrows(), 1):
                            with st.container():
                                st.markdown(f"""
                                    <div class='movie-card'>
                                        <h4 style='color: #E50914;'>{i}. {get_field(film, ['Phim', 'Tên Phim', 'title'])}</h4>
                                        <p><strong>🎯 Cụm:</strong> {cluster_value}</p>
                                        <p><strong>📅 Năm:</strong> {get_field(film, ['Năm', 'year'])}</p>
                                        <p><strong>🎭 Đạo diễn:</strong> {get_field(film, ['Đạo diễn', 'director'])}</p>
                                    </div>
                                """, unsafe_allow_html=True)

                                content = get_field(film, ['Content', 'Nội dung'])
                                st.write(snippet(content, 200))
                                if isinstance(content, str) and content.strip():
                                    with st.expander("📖 Đọc thêm"):
                                        st.write(content)
                                st.markdown("---")
                    else:
                        st.error("Chưa có dữ liệu phân cụm")

# Phim hay
elif menu == "⭐ Phim hay":
    st.markdown("<h1 style='text-align:center; color:#E50914;'>⭐ PHIM HAY ĐỀ XUẤT</h1>", unsafe_allow_html=True)
    st.markdown("---")

    if df is not None:
        if 'Doanh thu (tỷ VNĐ)' in df.columns:
            top_films = df.nlargest(12, 'Doanh thu (tỷ VNĐ)')
        else:
            top_films = df.head(12)

        cols = st.columns(3)
        for i, (idx, film) in enumerate(top_films.iterrows()):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class='movie-card'>
                        <h4 style='color: #E50914;'>{get_field(film, ['Phim', 'Tên Phim', 'title'])}</h4>
                        <p><strong>📅 Năm:</strong> {get_field(film, ['Năm', 'year'])}</p>
                        <p><strong>🎭 Đạo diễn:</strong> {get_field(film, ['Đạo diễn', 'director'])}</p>
                """, unsafe_allow_html=True)

                if 'Doanh thu (tỷ VNĐ)' in film.index:
                    st.markdown(f"<p><strong>💰 Doanh thu:</strong> {film['Doanh thu (tỷ VNĐ)']} tỷ</p>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                content = get_field(film, ['Content', 'Nội dung'])
                st.write(snippet(content, 150))
                if isinstance(content, str) and content.strip():
                    with st.expander("📖 Đọc thêm"):
                        st.write(content)

# Phân cụm phim
elif menu == "📊 Phân cụm phim":
    st.markdown("<h1 style='text-align:center; color:#E50914;'>📊 PHÂN CỤM NỘI DUNG PHIM</h1>", unsafe_allow_html=True)
    st.markdown("---")

    if df is not None and 'cluster' in df.columns:
        st.markdown("### 📈 Thống kê phân cụm")

        cluster_counts = df['cluster'].value_counts().sort_index()

        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(cluster_counts)
        with col2:
            st.markdown("#### 📊 Số lượng phim theo cụm")
            for cluster, count in cluster_counts.items():
                st.metric(f"Cụm {cluster}", f"{count} phim")

        st.markdown("---")
        st.markdown("### 🎯 Xem phim theo cụm")

        selected_cluster = st.selectbox(
            "Chọn cụm để xem danh sách phim:",
            options=sorted(df['cluster'].unique())
        )

        cluster_films = df[df['cluster'] == selected_cluster]
        st.info(f"🎬 Cụm #{selected_cluster} có {len(cluster_films)} phim")

        cols = st.columns(2)
        for i, (idx, film) in enumerate(cluster_films.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                    <div class='movie-card'>
                        <h4 style='color: #E50914;'>{get_field(film, ['Phim', 'Tên Phim', 'title'])}</h4>
                        <p><strong>📅 Năm:</strong> {get_field(film, ['Năm', 'year'])}</p>
                        <p><strong>🎭 Đạo diễn:</strong> {get_field(film, ['Đạo diễn', 'director'])}</p>
                    </div>
                """, unsafe_allow_html=True)

                content = get_field(film, ['Content', 'Nội dung'])
                st.write(snippet(content, 150))
                if isinstance(content, str) and content.strip():
                    with st.expander("📖 Đọc thêm"):
                        st.write(content)
    else:
        st.error("Chưa có dữ liệu phân cụm")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:#888; padding: 20px;'>
        <p>🎬 Hệ thống Gợi ý Phim Việt Nam | Powered by Machine Learning & AI</p>
        <p>Sử dụng TF-IDF, Cosine Similarity và K-Means Clustering</p>
    </div>
""", unsafe_allow_html=True)
