
# import streamlit as st
# import pandas as pd
# from PIL import Image
# import requests
# from io import BytesIO
# import plotly.express as px
# import os

# # -----------------------------
# # إعداد الصفحة
# # -----------------------------
# st.set_page_config(page_title="📚 Ultimate Books Dashboard", page_icon="📖", layout="wide")
# st.title("📚 Ultimate Books Dashboard")
# st.markdown("---")

# # -----------------------------
# # تحميل وتنظيف البيانات
# # -----------------------------
# # قمنا بتغيير اسم الدالة لكي يقوم Streamlit بتحديث البيانات فوراً
# @st.cache_data
# def load_books_data_v4():
#     df = pd.read_excel("books_portfolio.xlsx")
    
#     # 1. تنظيف السعر: إزالة الرموز الغريبة مثل (Â£) الظاهرة في الصورة وترك الأرقام
#     df["Price"] = df["Price"].astype(str).str.replace(r"[^\d.]", "", regex=True)
#     df["Price"] = pd.to_numeric(df["Price"], errors='coerce').fillna(0.0)
    
#     # 2. تنظيف التقييم: دالة جديدة تعد رموز النجوم الموجودة في الخلية
#     def count_stars(val):
#         val_str = str(val).strip()
#         # عد أي رموز نجوم ظاهرة في الإكسيل
#         stars = val_str.count('★') + val_str.count('⭐') + val_str.count('*')
#         if stars > 0:
#             return min(stars, 5)
            
#         # إذا كانت النجمة مخزنة كرمز يونيكود مختلف، نعد الرموز غير النصية في الخلية
#         symbols = [c for c in val_str if not c.isalnum() and not c.isspace()]
#         if len(symbols) > 0:
#             return min(len(symbols), 5)
            
#         return 1 # لو لم يجد شيء يضع نجمة واحدة

#     # تطبيق الدالة
#     df["Rating"] = df["Rating"].apply(count_stars)
    
#     return df

# # تحميل الداتا
# df = load_books_data_v4()

# # -----------------------------
# # Sidebar لتصفية البيانات
# # -----------------------------
# st.sidebar.header("🔍 الفلاتر وتصفية البيانات")

# min_price = st.sidebar.number_input("أقل سعر", min_value=0.0, value=float(df["Price"].min()))
# max_price = st.sidebar.number_input("أعلى سعر", min_value=0.0, value=float(df["Price"].max()))

# # فلتر التقييم
# selected_ratings = st.sidebar.multiselect(
#     "التقييم بالنجوم", 
#     options=[1, 2, 3, 4, 5], 
#     default=[1, 2, 3, 4, 5],
#     format_func=lambda x: f"{x} {'⭐' * x}"
# )

# keyword = st.sidebar.text_input("بحث باسم الكتاب أو الكلمة المفتاحية")

# # -----------------------------
# # تطبيق الفلاتر
# # -----------------------------
# df_filtered = df[
#     (df["Price"] >= min_price) &
#     (df["Price"] <= max_price) &
#     (df["Rating"].isin(selected_ratings))
# ]

# if keyword:
#     df_filtered = df_filtered[df_filtered["Name"].str.contains(keyword, case=False, na=False)]

# # -----------------------------
# # قسم الإحصائيات (KPIs) 
# # -----------------------------
# col1, col2, col3 = st.columns(3)
# col1.metric("📚 إجمالي الكتب المعروضة", f"{df_filtered.shape[0]} كتاب")
# col2.metric("💰 متوسط الأسعار", f"£ {df_filtered['Price'].mean():.2f}" if not df_filtered.empty else "£ 0.00")

# if not df_filtered.empty:
#     mode_val = int(df_filtered['Rating'].mode()[0])
#     mode_display = f"{mode_val} نجوم ({'⭐' * mode_val})"
# else:
#     mode_display = "لا يوجد"
    
# col3.metric("⭐ التقييم الأكثر شيوعاً", mode_display)

# st.markdown("---")

# # -----------------------------
# # تنظيم العرض في تبويبات
# # -----------------------------
# tab1, tab2 = st.tabs(["📊 التحليلات والرسوم البيانية", "📖 معرض الكتب"])

# # --- التبويب الأول: التحليلات ---
# with tab1:
#     if not df_filtered.empty:
#         col_chart1, col_chart2 = st.columns(2)
        
#         with col_chart1:
#             st.subheader("💰 توزيع أسعار الكتب")
#             # تم التأكد من ربط الرسم البياني بالداتا المفلترة df_filtered
#             fig_price = px.histogram(df_filtered, x="Price", nbins=20, 
#                                      color_discrete_sequence=['#636EFA'],
#                                      labels={'Price':'السعر (£)'})
#             fig_price.update_layout(yaxis_title="عدد الكتب", xaxis_title="السعر (£)")
#             st.plotly_chart(fig_price, use_container_width=True)

#         with col_chart2:
#             st.subheader("⭐ توزيع التقييمات")
#             rating_counts = df_filtered["Rating"].value_counts().reset_index()
#             rating_counts.columns = ["Rating", "Count"]
#             rating_counts = rating_counts.sort_values("Rating")
#             rating_counts["Rating_Label"] = rating_counts["Rating"].apply(lambda x: f"{x} نجوم")
            
#             fig_rating = px.pie(rating_counts, names="Rating_Label", values="Count", 
#                                 hole=0.4, color_discrete_sequence=px.colors.sequential.Plotly3)
#             st.plotly_chart(fig_rating, use_container_width=True)
#     else:
#         st.warning("⚠️ لا توجد بيانات تتطابق مع الفلاتر المحددة لعرض التحليلات.")

# # --- التبويب الثاني: معرض الكتب ---
# with tab2:
#     st.subheader("📖 تصفح الكتب")
#     if not df_filtered.empty:
#         cols = st.columns(4)
#         for i, (idx, row) in enumerate(df_filtered.iterrows()):
#             col = cols[i % 4]
#             with col:
#                 st.markdown(f"**{row['Name']}**")
                
#                 # التعامل مع الصور المفقودة (Failed to download) بأمان
#                 img_path = str(row["Image Path"])
#                 try:
#                     if img_path.startswith("http"):
#                         response = requests.get(img_path)
#                         img = Image.open(BytesIO(response.content))
#                         st.image(img, use_container_width=True)
#                     elif "failed" in img_path.lower():
#                         st.info("🚫 الصورة لم تُحمل")
#                     elif os.path.exists(img_path):
#                         img = Image.open(img_path)
#                         st.image(img, use_container_width=True)
#                     else:
#                         # محاولة عكس مسار الويندوز (\) إلى مسار عام (/)
#                         alt_path = img_path.replace("\\", "/")
#                         if os.path.exists(alt_path):
#                             img = Image.open(alt_path)
#                             st.image(img, use_container_width=True)
#                         else:
#                             st.info("🚫 مسار الصورة غير صحيح")
#                 except:
#                     st.info("🚫 خطأ في عرض الصورة")
                
#                 st.markdown(f"**السعر:** £{row['Price']}")
#                 st.markdown(f"**التقييم:** {'⭐' * int(row['Rating'])}")
#                 st.markdown(f"[🔗 رابط الكتاب]({row['Link']})")
#                 st.markdown("---")
#     else:
#         st.info("لا توجد كتب تطابق بحثك حالياً. جرب تغيير الفلاتر من القائمة الجانبية.")

# # -----------------------------
# # تذييل الصفحة
# # -----------------------------
# st.markdown("<br><br>", unsafe_allow_html=True)
# st.success("✅ Dashboard جاهزة! الداتا تم تحليلها وقراءتها بنجاح.")




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
# 2. تحميل وتنظيف البيانات (النسخة الذكية)
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
# 3. القائمة الجانبية (Sidebar)
# -----------------------------
# قسم "عن المشروع" لزيادة الاحترافية
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

# الفلاتر الأساسية
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

# ميزة الترتيب (Sorting)
sort_option = st.sidebar.selectbox(
    "ترتيب الكتب حسب:", 
    ["الافتراضي", "السعر: من الأرخص للأغلى ⬇️", "السعر: من الأغلى للأرخص ⬆️", "الأعلى تقييماً ⭐"]
)

# ميزة تحديد عدد النتائج (Pagination / Limit) لتسريع العرض
display_limit = st.sidebar.slider("عدد الكتب المعروضة في الصفحة", min_value=10, max_value=200, value=40)

# -----------------------------
# 4. معالجة البيانات (تطبيق الفلاتر والترتيب)
# -----------------------------
df_filtered = df[
    (df["Price"] >= min_price) &
    (df["Price"] <= max_price) &
    (df["Rating"].isin(selected_ratings))
]

if keyword:
    df_filtered = df_filtered[df_filtered["Name"].str.contains(keyword, case=False, na=False)]

# تطبيق الترتيب
if sort_option == "السعر: من الأرخص للأغلى ⬇️":
    df_filtered = df_filtered.sort_values(by="Price", ascending=True)
elif sort_option == "السعر: من الأغلى للأرخص ⬆️":
    df_filtered = df_filtered.sort_values(by="Price", ascending=False)
elif sort_option == "الأعلى تقييماً ⭐":
    df_filtered = df_filtered.sort_values(by=["Rating", "Price"], ascending=[False, True])

# -----------------------------
# زر التصدير (Export to CSV) في أسفل القائمة الجانبية
# -----------------------------
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
st.markdown("لوحة تحكم تفاعلية لتحليل بيانات متجر الكتب والمبيعات.")

# قسم الإحصائيات (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"📚 إجمالي الكتب: **{df_filtered.shape[0]}**")
with col2:
    st.success(f"💰 متوسط الأسعار: **£ {df_filtered['Price'].mean():.2f}**" if not df_filtered.empty else "💰 متوسط الأسعار: **£ 0.00**")
with col3:
    mode_val = int(df_filtered['Rating'].mode()[0]) if not df_filtered.empty else 0
    st.warning(f"⭐ التقييم الشائع: **{mode_val} نجوم**")

st.markdown("---")

# تنظيم العرض في تبويبات
tab1, tab2 = st.tabs(["📊 التحليلات المتقدمة", "📖 معرض الكتب السريع"])

# --- التبويب الأول: التحليلات ---
with tab1:
    if not df_filtered.empty:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig_price = px.histogram(df_filtered, x="Price", nbins=20, 
                                     color_discrete_sequence=['#3498db'],
                                     title="توزيع أسعار الكتب")
            fig_price.update_layout(xaxis_title="السعر (£)", yaxis_title="عدد الكتب", template="plotly_white")
            st.plotly_chart(fig_price, use_container_width=True)

        with col_chart2:
            rating_counts = df_filtered["Rating"].value_counts().reset_index()
            rating_counts.columns = ["Rating", "Count"]
            rating_counts = rating_counts.sort_values("Rating")
            rating_counts["Rating_Label"] = rating_counts["Rating"].apply(lambda x: f"{x} نجوم")
            
            fig_rating = px.pie(rating_counts, names="Rating_Label", values="Count", 
                                hole=0.45, title="نسبة التقييمات",
                                color_discrete_sequence=px.colors.sequential.Teal)
            st.plotly_chart(fig_rating, use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات تتطابق مع الفلاتر المحددة.")


# --- التبويب الثاني: معرض الكتب (باستخدام CSS) ---
with tab2:
    if not df_filtered.empty:
        # أخذ عدد محدد من الكتب لتسريع التصفح بناءً على الشريط الجانبي
        df_display = df_filtered.head(display_limit)
        st.caption(f"عرض أول {len(df_display)} كتاب من أصل {len(df_filtered)} لتسريع الأداء.")
        
        # تحويل البيانات لقائمة عشان نلف عليها صف بصف
        df_display_list = df_display.to_dict('records')
        num_columns = 4
        
        # بناء الشبكة (Grid) صف بصف عشان الكتب تكون على استقامة واحدة
        for i in range(0, len(df_display_list), num_columns):
            cols = st.columns(num_columns) # بنعمل صف جديد لكل 4 كتب
            
            for j in range(num_columns):
                if i + j < len(df_display_list):
                    row = df_display_list[i + j]
                    with cols[j]:
                        img_url = str(row.get("Image URL", ""))
                        
                        # لو مفيش رابط إنترنت للصورة، هنستخدم صورة بيضاء كبديل
                        if not img_url.startswith("http"):
                            img_url = "https://via.placeholder.com/200x300.png?text=No+Image&bg=ffffff&textcolor=cccccc"
                        
                        # لاحظ هنا: شلنا كل المسافات اللي قبل الـ HTML عشان ميتحولش لنص
                        card_html = f"""
<div style='padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center; margin-bottom: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); height: 420px; display: flex; flex-direction: column; background-color: white;'>
    <div style='height: 200px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;'>
        <img src='{img_url}' style='max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 5px;' onerror="this.src='https://via.placeholder.com/200x300.png?text=Error&bg=ffffff'">
    </div>
    <div style='flex-grow: 1;'>
        <h5 style='font-size: 14px; height: 40px; overflow: hidden; margin: 0 0 10px 0;'>{row.get('Name', 'بدون اسم')}</h5>
        <h3 style='color: #27ae60; margin: 5px 0;'>£ {row.get('Price', '0.0')}</h3>
        <p style='margin: 5px 0; font-size: 14px;'>{'⭐' * int(row.get('Rating', 1))}</p>
    </div>
    <a href='{row.get('Link', '#')}' target='_blank' style='display: block; width: 100%; padding: 8px 0; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; font-size: 13px; font-weight: bold;'>رابط الكتاب</a>
</div>
"""
                        st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("لا توجد كتب تطابق بحثك حالياً.")
# -----------------------------
# 6. تذييل الصفحة
# -----------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>تم التطوير باحترافية لعرض البيانات الضخمة </p>", unsafe_allow_html=True)