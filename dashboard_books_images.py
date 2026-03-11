
# import streamlit as st
# import pandas as pd
# from PIL import Image
# import requests
# from io import BytesIO
# import plotly.express as px
# import os

# # -----------------------------
# # 1. إعداد الصفحة (يجب أن يكون أول سطر)
# # -----------------------------
# st.set_page_config(page_title="📚 Books Dashboard", page_icon="📖", layout="wide")

# # -----------------------------
# # 2. تحميل وتنظيف البيانات (النسخة الذكية)
# # -----------------------------
# @st.cache_data
# def load_books_data_pro():
#     df = pd.read_excel("books_portfolio.xlsx")
    
#     # تنظيف السعر
#     df["Price"] = df["Price"].astype(str).str.replace(r"[^\d.]", "", regex=True)
#     df["Price"] = pd.to_numeric(df["Price"], errors='coerce').fillna(0.0)
    
#     # تنظيف التقييم (عد النجوم الموجودة في الإكسيل)
#     def count_stars(val):
#         val_str = str(val).strip()
#         stars = val_str.count('★') + val_str.count('⭐') + val_str.count('*')
#         if stars > 0: return min(stars, 5)
        
#         symbols = [c for c in val_str if not c.isalnum() and not c.isspace()]
#         if len(symbols) > 0: return min(len(symbols), 5)
#         return 1 

#     df["Rating"] = df["Rating"].apply(count_stars)
#     return df

# df = load_books_data_pro()

# # -----------------------------
# # 3. القائمة الجانبية (Sidebar)
# # -----------------------------
# # قسم "عن المشروع" لزيادة الاحترافية
# with st.sidebar.expander("ℹ️ عن هذا المشروع", expanded=True):
#     st.write("""
#     **لوحة تحكم تفاعلية متكاملة**
#     - تم سحب البيانات (Web Scraping).
#     - تنظيف البيانات باستخدام **Pandas**.
#     - الرسوم البيانية باستخدام **Plotly**.
#     - تطوير الواجهة باستخدام **Streamlit**.
#     """)

# st.sidebar.markdown("---")
# st.sidebar.header("🔍 الفلاتر وتصفية البيانات")

# # الفلاتر الأساسية
# min_price = st.sidebar.number_input("أقل سعر (£)", min_value=0.0, value=float(df["Price"].min()))
# max_price = st.sidebar.number_input("أعلى سعر (£)", min_value=0.0, value=float(df["Price"].max()))

# selected_ratings = st.sidebar.multiselect(
#     "التقييم بالنجوم", 
#     options=[1, 2, 3, 4, 5], 
#     default=[1, 2, 3, 4, 5],
#     format_func=lambda x: f"{x} {'⭐' * x}"
# )

# keyword = st.sidebar.text_input("بحث باسم الكتاب...")

# st.sidebar.markdown("---")
# st.sidebar.header("⚙️ إعدادات العرض")

# # ميزة الترتيب (Sorting)
# sort_option = st.sidebar.selectbox(
#     "ترتيب الكتب حسب:", 
#     ["الافتراضي", "السعر: من الأرخص للأغلى ⬇️", "السعر: من الأغلى للأرخص ⬆️", "الأعلى تقييماً ⭐"]
# )

# # ميزة تحديد عدد النتائج (Pagination / Limit) لتسريع العرض
# display_limit = st.sidebar.slider("عدد الكتب المعروضة في الصفحة", min_value=10, max_value=200, value=40)

# # -----------------------------
# # 4. معالجة البيانات (تطبيق الفلاتر والترتيب)
# # -----------------------------
# df_filtered = df[
#     (df["Price"] >= min_price) &
#     (df["Price"] <= max_price) &
#     (df["Rating"].isin(selected_ratings))
# ]

# if keyword:
#     df_filtered = df_filtered[df_filtered["Name"].str.contains(keyword, case=False, na=False)]

# # تطبيق الترتيب
# if sort_option == "السعر: من الأرخص للأغلى ⬇️":
#     df_filtered = df_filtered.sort_values(by="Price", ascending=True)
# elif sort_option == "السعر: من الأغلى للأرخص ⬆️":
#     df_filtered = df_filtered.sort_values(by="Price", ascending=False)
# elif sort_option == "الأعلى تقييماً ⭐":
#     df_filtered = df_filtered.sort_values(by=["Rating", "Price"], ascending=[False, True])

# # -----------------------------
# # زر التصدير (Export to CSV) في أسفل القائمة الجانبية
# # -----------------------------
# st.sidebar.markdown("---")
# st.sidebar.subheader("📥 تصدير التقرير")
# csv_data = df_filtered.to_csv(index=False).encode('utf-8')
# st.sidebar.download_button(
#     label="تحميل البيانات المفلترة (CSV)",
#     data=csv_data,
#     file_name='books_report.csv',
#     mime='text/csv',
# )

# # -----------------------------
# # 5. الواجهة الرئيسية للـ Dashboard
# # -----------------------------
# st.title("📚 Books Dashboard")
# st.markdown("لوحة تحكم تفاعلية لتحليل بيانات متجر الكتب والمبيعات.")

# # قسم الإحصائيات (KPIs)
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.info(f"📚 إجمالي الكتب: **{df_filtered.shape[0]}**")
# with col2:
#     st.success(f"💰 متوسط الأسعار: **£ {df_filtered['Price'].mean():.2f}**" if not df_filtered.empty else "💰 متوسط الأسعار: **£ 0.00**")
# with col3:
#     mode_val = int(df_filtered['Rating'].mode()[0]) if not df_filtered.empty else 0
#     st.warning(f"⭐ التقييم الشائع: **{mode_val} نجوم**")

# st.markdown("---")

# # تنظيم العرض في تبويبات
# tab1, tab2 = st.tabs(["📊 التحليلات المتقدمة", "📖 معرض الكتب السريع"])

# # --- التبويب الأول: التحليلات ---
# with tab1:
#     if not df_filtered.empty:
#         col_chart1, col_chart2 = st.columns(2)
        
#         with col_chart1:
#             fig_price = px.histogram(df_filtered, x="Price", nbins=20, 
#                                      color_discrete_sequence=['#3498db'],
#                                      title="توزيع أسعار الكتب")
#             fig_price.update_layout(xaxis_title="السعر (£)", yaxis_title="عدد الكتب", template="plotly_white")
#             st.plotly_chart(fig_price, use_container_width=True)

#         with col_chart2:
#             rating_counts = df_filtered["Rating"].value_counts().reset_index()
#             rating_counts.columns = ["Rating", "Count"]
#             rating_counts = rating_counts.sort_values("Rating")
#             rating_counts["Rating_Label"] = rating_counts["Rating"].apply(lambda x: f"{x} نجوم")
            
#             fig_rating = px.pie(rating_counts, names="Rating_Label", values="Count", 
#                                 hole=0.45, title="نسبة التقييمات",
#                                 color_discrete_sequence=px.colors.sequential.Teal)
#             st.plotly_chart(fig_rating, use_container_width=True)
#     else:
#         st.warning("⚠️ لا توجد بيانات تتطابق مع الفلاتر المحددة.")


# # --- التبويب الثاني: معرض الكتب (باستخدام CSS) ---
# with tab2:
#     if not df_filtered.empty:
#         # أخذ عدد محدد من الكتب لتسريع التصفح بناءً على الشريط الجانبي
#         df_display = df_filtered.head(display_limit)
#         st.caption(f"عرض أول {len(df_display)} كتاب من أصل {len(df_filtered)} لتسريع الأداء.")
        
#         # تحويل البيانات لقائمة عشان نلف عليها صف بصف
#         df_display_list = df_display.to_dict('records')
#         num_columns = 4
        
#         # بناء الشبكة (Grid) صف بصف عشان الكتب تكون على استقامة واحدة
#         for i in range(0, len(df_display_list), num_columns):
#             cols = st.columns(num_columns) # بنعمل صف جديد لكل 4 كتب
            
#             for j in range(num_columns):
#                 if i + j < len(df_display_list):
#                     row = df_display_list[i + j]
#                     with cols[j]:
#                         img_url = str(row.get("Image URL", ""))
                        
#                         # لو مفيش رابط إنترنت للصورة، هنستخدم صورة بيضاء كبديل
#                         if not img_url.startswith("http"):
#                             img_url = "https://via.placeholder.com/200x300.png?text=No+Image&bg=ffffff&textcolor=cccccc"
                        
#                         # لاحظ هنا: شلنا كل المسافات اللي قبل الـ HTML عشان ميتحولش لنص
#                         card_html = f"""
# <div style='padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center; margin-bottom: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 420px; display: flex; flex-direction: column; background-color: white;'>
#     <div style='height: 200px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;'>
#         <img src='{img_url}' style='max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 5px;' onerror="this.src='https://via.placeholder.com/200x300.png?text=Error&bg=ffffff'">
#     </div>
#     <div style='flex-grow: 1;'>
#         <h5 style='font-size: 14px; height: 40px; overflow: hidden; margin: 0 0 10px 0;'>{row.get('Name', 'بدون اسم')}</h5>
#         <h3 style='color: #27ae60; margin: 5px 0;'>£ {row.get('Price', '0.0')}</h3>
#         <p style='margin: 5px 0; font-size: 14px;'>{'⭐' * int(row.get('Rating', 1))}</p>
#     </div>
#     <a href='{row.get('Link', '#')}' target='_blank' style='display: block; width: 100%; padding: 8px 0; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; font-size: 13px; font-weight: bold;'>رابط الكتاب</a>
# </div>
# """
#                         st.markdown(card_html, unsafe_allow_html=True)
#     else:
#         st.info("لا توجد كتب تطابق بحثك حالياً.")
# # -----------------------------
# # 6. تذييل الصفحة
# # -----------------------------
# st.markdown("<br>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center; color: gray;'>تم التطوير باحترافية لعرض البيانات الضخمة </p>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px
import os

# -----------------------------
# 1. إعداد الصفحة (يجب أن يكون أول سطر)
# -----------------------------
st.set_page_config(page_title="📚 Books Dashboard", page_icon="📖", layout="wide")

# -----------------------------
# حقن كود CSS مخصص للحصول على تصميم احترافي (UI/UX)
# -----------------------------
st.markdown("""
<style>
    /* جعل الخلفية تتكيف مع الوضع الليلي/النهاري تلقائياً */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* تصميم بطاقات الإحصائيات (KPIs) */
    .nova-card {
        background-color: var(--secondary-background-color); /* لون متغير حسب الوضع */
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #7367f0;
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out;
    }
    .nova-card:hover {
        transform: translateY(-5px);
    }
    .nova-card-title {
        color: var(--text-color);
        opacity: 0.8; /* لتقليل حدة النص قليلاً وجعله أنيقاً */
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .nova-card-value {
        color: var(--text-color);
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .nova-card-trend {
        color: #28c76f;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* تصميم بطاقات الكتب */
    .book-card {
        padding: 15px; 
        border-radius: 12px; 
        border: 1px solid rgba(128, 128, 128, 0.2); /* حدود خفيفة جداً تظهر في الدارك مود */
        text-align: center; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); 
        height: 420px; 
        display: flex; 
        flex-direction: column; 
        background-color: var(--secondary-background-color); /* تتكيف مع الوضع */
        color: var(--text-color);
        transition: box-shadow 0.3s ease;
    }
    .book-card:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* إجبار عناوين الكتب على التكيف مع الوضع الليلي وتخطي الألوان المكتوبة في بايثون */
    .book-card h5 {
        color: var(--text-color) !important;
    }
    
    /* زر رابط الكتاب بدون خط سفلي */
    .book-btn {
        display: block; 
        width: 100%; 
        padding: 10px 0; 
        background-color: #7367f0; 
        color: white !important; 
        text-decoration: none !important; /* إزالة الخط السفلي */
        border-radius: 6px; 
        font-size: 14px; 
        font-weight: bold;
        transition: background-color 0.2s;
    }
    .book-btn:hover {
        background-color: #5e50ee;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 2. تحميل وتنظيف البيانات (نفس الكود الخاص بك بالضبط)
# -----------------------------
@st.cache_data
def load_books_data_pro():
    df = pd.read_excel("books_portfolio.xlsx")
    
    # تنظيف السعر
    df["Price"] = df["Price"].astype(str).str.replace(r"[^\d.]", "", regex=True)
    df["Price"] = pd.to_numeric(df["Price"], errors='coerce').fillna(0.0)
    
    # تنظيف التقييم (عد النجوم الموجودة في الإكسيل)
    def count_stars(val):
        val_str = str(val).strip()
        stars = val_str.count('★') + val_str.count('⭐') + val_str.count('*')
        if stars > 0: return min(stars, 5)
        
        symbols = [c for c in val_str if not c.isalnum() and not c.isspace()]
        if len(symbols) > 0: return min(len(symbols), 5)
        return 1 

    df["Rating"] = df["Rating"].apply(count_stars)
    return df

df = load_books_data_pro()

# -----------------------------
# 3. القائمة الجانبية (Sidebar) (نفس الكود الخاص بك)
# -----------------------------
with st.sidebar.expander("ℹ️ عن هذا المشروع", expanded=True):
    st.write("""
    **لوحة تحكم تفاعلية متكاملة**
    - تم سحب البيانات (Web Scraping).
    - تنظيف البيانات باستخدام **Pandas**.
    - الرسوم البيانية باستخدام **Plotly**.
    - تطوير الواجهة باستخدام **Streamlit**.
    """)

st.sidebar.markdown("---")
st.sidebar.header("🔍 الفلاتر وتصفية البيانات")

min_price = st.sidebar.number_input("أقل سعر (£)", min_value=0.0, value=float(df["Price"].min()))
max_price = st.sidebar.number_input("أعلى سعر (£)", min_value=0.0, value=float(df["Price"].max()))

selected_ratings = st.sidebar.multiselect(
    "التقييم بالنجوم", 
    options=[1, 2, 3, 4, 5], 
    default=[1, 2, 3, 4, 5],
    format_func=lambda x: f"{x} {'⭐' * x}"
)

keyword = st.sidebar.text_input("بحث باسم الكتاب...")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ إعدادات العرض")

sort_option = st.sidebar.selectbox(
    "ترتيب الكتب حسب:", 
    ["الافتراضي", "السعر: من الأرخص للأغلى ⬇️", "السعر: من الأغلى للأرخص ⬆️", "الأعلى تقييماً ⭐"]
)

display_limit = st.sidebar.slider("عدد الكتب المعروضة في الصفحة", min_value=10, max_value=200, value=40)

# -----------------------------
# 4. معالجة البيانات (نفس الكود الخاص بك)
# -----------------------------
df_filtered = df[
    (df["Price"] >= min_price) &
    (df["Price"] <= max_price) &
    (df["Rating"].isin(selected_ratings))
]

if keyword:
    df_filtered = df_filtered[df_filtered["Name"].str.contains(keyword, case=False, na=False)]

if sort_option == "السعر: من الأرخص للأغلى ⬇️":
    df_filtered = df_filtered.sort_values(by="Price", ascending=True)
elif sort_option == "السعر: من الأغلى للأرخص ⬆️":
    df_filtered = df_filtered.sort_values(by="Price", ascending=False)
elif sort_option == "الأعلى تقييماً ⭐":
    df_filtered = df_filtered.sort_values(by=["Rating", "Price"], ascending=[False, True])

# زر التصدير
st.sidebar.markdown("---")
st.sidebar.subheader("📥 تصدير التقرير")
csv_data = df_filtered.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="تحميل البيانات المفلترة (CSV)",
    data=csv_data,
    file_name='books_report.csv',
    mime='text/csv',
)

# -----------------------------
# 5. الواجهة الرئيسية للـ Dashboard
# -----------------------------
st.title("📚 Books Dashboard")
st.markdown("<p style='color: #6e6b7b; margin-top: -15px; margin-bottom: 30px;'>لوحة تحكم تفاعلية لتحليل بيانات متجر الكتب والمبيعات.</p>", unsafe_allow_html=True)

# --- قسم الإحصائيات بتصميم احترافي UI ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="nova-card">
        <div class="nova-card-title">إجمالي الكتب المتاحة</div>
        <div class="nova-card-value">{df_filtered.shape[0]:,}</div>
        <div class="nova-card-trend">↑ محدث تلقائياً</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_price = df_filtered['Price'].mean() if not df_filtered.empty else 0
    st.markdown(f"""
    <div class="nova-card" style="border-top-color: #00cfe8;">
        <div class="nova-card-title">متوسط أسعار الكتب</div>
        <div class="nova-card-value">£ {avg_price:.2f}</div>
        <div class="nova-card-trend" style="color: #00cfe8;">~ استقرار</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    mode_val = int(df_filtered['Rating'].mode()[0]) if not df_filtered.empty else 0
    st.markdown(f"""
    <div class="nova-card" style="border-top-color: #ff9f43;">
        <div class="nova-card-title">التقييم الشائع</div>
        <div class="nova-card-value">{mode_val} نجوم</div>
        <div class="nova-card-trend" style="color: #ff9f43;">★ تقييمات</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 التحليلات المتقدمة", "📖 معرض الكتب السريع"])

# --- التبويب الأول: التحليلات ---
with tab1:
    if not df_filtered.empty:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig_price = px.histogram(df_filtered, x="Price", nbins=20, 
                                     color_discrete_sequence=['#7367f0'], 
                                     title="توزيع أسعار الكتب")
            fig_price.update_layout(
                xaxis_title="السعر (£)", 
                yaxis_title="", 
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=50, b=20),
                title_font=dict(size=18, color='#5e5873')
            )
            st.plotly_chart(fig_price, use_container_width=True)


        with col_chart2:
            rating_counts = df_filtered["Rating"].value_counts().reset_index()
            rating_counts.columns = ["Rating", "Count"]
            rating_counts = rating_counts.sort_values("Rating")
            rating_counts["Rating_Label"] = rating_counts["Rating"].apply(lambda x: f"{x} نجوم")
            
            nova_colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#7367f0']
            
            fig_rating = px.pie(rating_counts, names="Rating_Label", values="Count", 
                                hole=0.55, title="نسبة التقييمات",
                                color_discrete_sequence=nova_colors)
            fig_rating.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=50, b=20),
                title_font=dict(size=18, color='#5e5873')
            )
            st.plotly_chart(fig_rating, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات تتطابق مع الفلاتر المحددة.")


# --- التبويب الثاني: معرض الكتب ---
with tab2:
    if not df_filtered.empty:
        df_display = df_filtered.head(display_limit)
        st.caption(f"عرض أول {len(df_display)} كتاب من أصل {len(df_filtered)} لتسريع الأداء.")
        
        df_display_list = df_display.to_dict('records')
        num_columns = 4
        
        for i in range(0, len(df_display_list), num_columns):
            cols = st.columns(num_columns) 
            
            for j in range(num_columns):
                if i + j < len(df_display_list):
                    row = df_display_list[i + j]
                    with cols[j]:
                        img_url = str(row.get("Image URL", ""))
                        if not img_url.startswith("http"):
                            img_url = "https://via.placeholder.com/200x300.png?text=No+Image&bg=f8f9fa&textcolor=a3aed1"
                        
                        card_html = f"""
                        <div class='book-card'>
                            <div style='height: 200px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;'>
                                <img src='{img_url}' style='max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px;' onerror="this.src='https://via.placeholder.com/200x300.png?text=Error&bg=ffffff'">
                            </div>
                            <div style='flex-grow: 1;'>
                                <h5 style='font-size: 15px; color: #5e5873; height: 40px; overflow: hidden; margin: 0 0 10px 0;'>{row.get('Name', 'بدون اسم')}</h5>
                                <h3 style='color: #7367f0; margin: 5px 0;'>£ {row.get('Price', '0.0')}</h3>
                                <p style='margin: 5px 0; font-size: 14px; color: #ff9f43;'>{'★' * int(row.get('Rating', 1))}</p>
                            </div>
                            <a href='{row.get('Link', '#')}' target='_blank' class='book-btn'>رابط الكتاب</a>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("لا توجد كتب تطابق بحثك حالياً.")

# -----------------------------
# 6. تذييل الصفحة
# -----------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3aed1; font-weight: bold;'>تم التطوير باحترافية لعرض البيانات الضخمة</p>", unsafe_allow_html=True)