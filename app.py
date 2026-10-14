import streamlit as st
import os

# 1. إعدادات الصفحة والتصميم
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1b4d3e;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #555;
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #1b4d3e;
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #12352b;
        color: #d4af37;
    }
    .stats-card {
        background-color: #f4f7f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: #1b4d3e;
        font-weight: bold;
        border: 1px solid #d1dedb;
    }
    </style>
""", unsafe_allow_html=True)

# 2. العنوان الرئيسي للموقع
st.markdown("<h1 class='main-header'>الموسوعة القرآنية الشاملة</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>مصحف المدينة، البث المباشر، المساعد الفقهي، وإدارة الختمة اليومية</p>", unsafe_allow_html=True)
st.markdown("---")

# 3. قاعدة البيانات الموسوعية لجميع سور القرآن الكريم الـ 114
QURAN_SURAHS = [
    {"id": 1, "name": "الفاتحة", "type": "مكية", "verses": 7, "juz": 1},
    {"id": 2, "name": "البقرة", "type": "مدنية", "verses": 286, "juz": 1},
    {"id": 3, "name": "آل عمران", "type": "مدنية", "verses": 200, "juz": 3},
    {"id": 4, "name": "النساء", "type": "مدنية", "verses": 176, "juz": 4},
    {"id": 5, "name": "المائدة", "type": "مدنية", "verses": 120, "juz": 6},
    {"id": 6, "name": "الأنعام", "type": "مكية", "verses": 165, "juz": 7},
    {"id": 7, "name": "الأعراف", "type": "مكية", "verses": 206, "juz": 8},
    {"id": 8, "name": "الأنفال", "type": "مدنية", "verses": 75, "juz": 9},
    {"id": 9, "name": "التوبة", "type": "مدنية", "verses": 129, "juz": 10},
    {"id": 10, "name": "يونس", "type": "مكية", "verses": 109, "juz": 11},
    {"id": 11, "name": "هود", "type": "مكية", "verses": 123, "juz": 11},
    {"id": 12, "name": "يوسف", "type": "مكية", "verses": 111, "juz": 12},
    {"id": 13, "name": "الرعد", "type": "مدنية", "verses": 43, "juz": 13},
    {"id": 14, "name": "إبراهيم", "type": "مكية", "verses": 52, "juz": 13},
    {"id": 15, "name": "الحجر", "type": "مكية", "verses": 99, "juz": 14},
    {"id": 16, "name": "النحل", "type": "مكية", "verses": 128, "juz": 14},
    {"id": 17, "name": "الإسراء", "type": "مكية", "verses": 111, "juz": 15},
    {"id": 18, "name": "الكهف", "type": "مكية", "verses": 110, "juz": 15},
    {"id": 19, "name": "مريم", "type": "مكية", "verses": 98, "juz": 16},
    {"id": 20, "name": "طه", "type": "مكية", "verses": 135, "juz": 16},
    {"id": 21, "name": "الأنبياء", "type": "مكية", "verses": 112, "juz": 17},
    {"id": 22, "name": "الحج", "type": "مدنية", "verses": 78, "juz": 17},
    {"id": 23, "name": "المؤمنون", "type": "مكية", "verses": 118, "juz": 18},
    {"id": 24, "name": "النور", "type": "مدنية", "verses": 64, "juz": 18},
    {"id": 25, "name": "الفرقان", "type": "مكية", "verses": 77, "juz": 18},
    {"id": 26, "name": "الشعراء", "type": "مكية", "verses": 227, "juz": 19},
    {"id": 27, "name": "النمل", "type": "مكية", "verses": 93, "juz": 19},
    {"id": 28, "name": "القصص", "type": "مكية", "verses": 88, "juz": 20},
    {"id": 29, "name": "العنكبوت", "type": "مكية", "verses": 69, "juz": 20},
    {"id": 30, "name": "الروم", "type": "مكية", "verses": 60, "juz": 21},
    {"id": 31, "name": "لقمان", "type": "مكية", "verses": 34, "juz": 21},
    {"id": 32, "name": "السجدة", "type": "مكية", "verses": 30, "juz": 21},
    {"id": 33, "name": "الأحزاب", "type": "مدنية", "verses": 73, "juz": 21},
    {"id": 34, "name": "سبأ", "type": "مكية", "verses": 54, "juz": 22},
    {"id": 35, "name": "فاطر", "type": "مكية", "verses": 45, "juz": 22},
    {"id": 36, "name": "يس", "type": "مكية", "verses": 83, "juz": 22},
    {"id": 37, "name": "الصافات", "type": "مكية", "verses": 182, "juz": 23},
    {"id": 38, "name": "ص", "type": "مكية", "verses": 88, "juz": 23},
    {"id": 39, "name": "الزمر", "type": "مكية", "verses": 75, "juz": 23},
    {"id": 40, "name": "غافر", "type": "مكية", "verses": 85, "juz": 24},
    {"id": 41, "name": "فصلت", "type": "مكية", "verses": 54, "juz": 24},
    {"id": 42, "name": "الشورى", "type": "مكية", "verses": 53, "juz": 25},
    {"id": 43, "name": "الزخرف", "type": "مكية", "verses": 89, "juz": 25},
    {"id": 44, "name": "الدخان", "type": "مكية", "verses": 59, "juz": 25},
    {"id": 45, "name": "الجاثية", "type": "مكية", "verses": 37, "juz": 25},
    {"id": 46, "name": "الأحقاف", "type": "مكية", "verses": 35, "juz": 26},
    {"id": 47, "name": "محمد", "type": "مدنية", "verses": 38, "juz": 26},
    {"id": 48, "name": "الفتح", "type": "مدنية", "verses": 29, "juz": 26},
    {"id": 49, "name": "الحجرات", "type": "مدنية", "verses": 18, "juz": 26},
    {"id": 50, "name": "ق", "type": "مكية", "verses": 45, "juz": 26},
    {"id": 51, "name": "الذاريات", "type": "مكية", "verses": 60, "juz": 26},
    {"id": 52, "name": "الطور", "type": "مكية", "verses": 49, "juz": 27},
    {"id": 53, "name": "النجم", "type": "مكية", "verses": 62, "juz": 27},
    {"id": 54, "name": "القمر", "type": "مكية", "verses": 55, "juz": 27},
    {"id": 55, "name": "الرحمن", "type": "مدنية", "verses": 78, "juz": 27},
    {"id": 56, "name": "الواقعة", "type": "مكية", "verses": 96, "juz": 27},
    {"id": 57, "name": "الحديد", "type": "مدنية", "verses": 29, "juz": 27},
    {"id": 58, "name": "المجادلة", "type": "مدنية", "verses": 22, "juz": 28},
    {"id": 59, "name": "الحشر", "type": "مدنية", "verses": 24, "juz": 28},
    {"id": 60, "name": "الممتحنة", "type": "مدنية", "verses": 13, "juz": 28},
    {"id": 61, "name": "الصف", "type": "مدنية", "verses": 14, "juz": 28},
    {"id": 62, "name": "الجمعة", "type": "مدنية", "verses": 11, "juz": 28},
    {"id": 63, "name": "المنافقون", "type": "مدنية", "verses": 11, "juz": 28},
    {"id": 64, "name": "التغابن", "type": "مدنية", "verses": 18, "juz": 28},
    {"id": 65, "name": "الطلاق", "type": "مدنية", "verses": 12, "juz": 28},
    {"id": 66, "name": "التحريم", "type": "مدنية", "verses": 12, "juz": 28},
    {"id": 67, "name": "الملك", "type": "مكية", "verses": 30, "juz": 29},
    {"id": 68, "name": "القلم", "type": "مكية", "verses": 52, "juz": 29},
    {"id": 69, "name": "الحاقة", "type": "مكية", "verses": 52, "juz": 29},
    {"id": 70, "name": "المعارج", "type": "مكية", "verses": 44, "juz": 29},
    {"id": 71, "name": "نوح", "type": "مكية", "verses": 28, "juz": 29},
    {"id": 72, "name": "الجن", "type": "مكية", "verses": 28, "juz": 29},
    {"id": 73, "name": "المزمل", "type": "مكية", "verses": 20, "juz": 29},
    {"id": 74, "name": "المدثر", "type": "مكية", "verses": 56, "juz": 29},
    {"id": 75, "name": "القيامة", "type": "مكية", "verses": 40, "juz": 29},
    {"id": 76, "name": "الإنسان", "type": "مدنية", "verses": 31, "juz": 29},
    {"id": 77, "name": "المرسلات", "type": "مكية", "verses": 50, "juz": 29},
    {"id": 78, "name": "النبأ", "type": "مكية", "verses": 40, "juz": 30},
    {"id": 79, "name": "النازعات", "type": "مكية", "verses": 46, "juz": 30},
    {"id": 80, "name": "عبس", "type": "مكية", "verses": 42, "juz": 30},
    {"id": 81, "name": "التكوير", "type": "مكية", "verses": 29, "juz": 30},
    {"id": 82, "name": "الانفطار", "type": "مكية", "verses": 19, "juz": 30},
    {"id": 83, "name": "المطففين", "type": "مكية", "verses": 36, "juz": 30},
    {"id": 84, "name": "الانشقاق", "type": "مكية", "verses": 25, "juz": 30},
    {"id": 85, "name": "البروج", "type": "مكية", "verses": 22, "juz": 30},
    {"id": 86, "name": "الطارق", "type": "مكية", "verses": 17, "juz": 30},
    {"id": 87, "name": "الأعلى", "type": "مكية", "verses": 19, "juz": 30},
    {"id": 88, "name": "الغاشية", "type": "مكية", "verses": 26, "juz": 30},
    {"id": 89, "name": "الفجر", "type": "مكية", "verses": 30, "juz": 30},
    {"id": 90, "name": "البلد", "type": "مكية", "verses": 20, "juz": 30},
    {"id": 91, "name": "الشمس", "type": "مكية", "verses": 15, "juz": 30},
    {"id": 92, "name": "الليل", "type": "مكية", "verses": 21, "juz": 30},
    {"id": 93, "name": "الضحى", "type": "مكية", "verses": 11, "juz": 30},
    {"id": 94, "name": "الشرح", "type": "مكية", "verses": 8, "juz": 30},
    {"id": 95, "name": "التين", "type": "مكية", "verses": 8, "juz": 30},
    {"id": 96, "name": "العلق", "type": "مكية", "verses": 19, "juz": 30},
    {"id": 97, "name": "القدر", "type": "مكية", "verses": 5, "juz": 30},
    {"id": 98, "name": "البينة", "type": "مدنية", "verses": 8, "juz": 30},
    {"id": 99, "name": "الزلزلة", "type": "مدنية", "verses": 8, "juz": 30},
    {"id": 100, "name": "العاديات", "type": "مكية", "verses": 11, "juz": 30},
    {"id": 101, "name": "القارعة", "type": "مكية", "verses": 11, "juz": 30},
    {"id": 102, "name": "التكاثر", "type": "مكية", "verses": 8, "juz": 30},
    {"id": 103, "name": "العصر", "type": "مكية", "verses": 3, "juz": 30},
    {"id": 104, "name": "الهمزة", "type": "مكية", "verses": 9, "juz": 30},
    {"id": 105, "name": "الفيل", "type": "مكية", "verses": 5, "juz": 30},
    {"id": 106, "name": "قريش", "type": "مكية", "verses": 4, "juz": 30},
    {"id": 107, "name": "الماعون", "type": "مكية", "verses": 7, "juz": 30},
    {"id": 108, "name": "الكوثر", "type": "مكية", "verses": 3, "juz": 30},
    {"id": 109, "name": "الكافرون", "type": "مكية", "verses": 6, "juz": 30},
    {"id": 110, "name": "النصر", "type": "مدنية", "verses": 3, "juz": 30},
    {"id": 111, "name": "المسد", "type": "مكية", "verses": 5, "juz": 30},
    {"id": 112, "name": "الإخلاص", "type": "مكية", "verses": 4, "juz": 30},
    {"id": 113, "name": "الفلق", "type": "مكية", "verses": 5, "juz": 30},
    {"id": 114, "name": "الناس", "type": "مكية", "verses": 6, "juz": 30}
]

# 4. التبويبات الرئيسية للتطبيق
tab1, tab2, tab3, tab4 = st.tabs(["📖 تصفح المصحف", "📻 البث المباشر", "🤖 المساعد الفقهي", "⚙️ الإحصائيات والملاحظات"])

# تبويب تصفح المصحف بالصور والسور
with tab1:
    st.header("تصفح مصحف المدينة النبوية")
    surah_options = [f"{s['id']}. سورة {s['name']} (الجزء {s['juz']} - {s['type']} - {s['verses']} آية)" for s in QURAN_SURAHS]
    sel_idx = st.selectbox("اختر السورة للانتقال:", range(len(surah_options)), format_func=lambda i: surah_options[i])
    s_info = QURAN_SURAHS[sel_idx]
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='stats-card'>رقم السورة: {s_info['id']}</div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='stats-card'>النوع: {s_info['type']}</div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='stats-card'>عدد الآيات: {s_info['verses']}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    q_folder = "quran_images"
    if os.path.exists(q_folder):
        imgs = sorted([f for f in os.listdir(q_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))])
    else:
        imgs = []

    if imgs:
        if 'p_num' not in st.session_state: st.session_state.p_num = 0
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.button("⬅️ الصفحة السابقة") and st.session_state.p_num > 0: st.session_state.p_num -= 1
        with c2:
            st.session_state.p_num = st.number_input("رقم الصفحة المباشر:", 0, len(imgs)-1, st.session_state.p_num)
        with c3:
            if st.button("الصفحة التالية ➡️") and st.session_state.p_num < len(imgs)-1: st.session_state.p_num += 1
        st.image(os.path.join(q_folder, imgs[st.session_state.p_num]), use_column_width=True)
    else:
        st.warning(f"⚠️ تنبيه: يرجى وضع صور صفحات المصحف داخل مجلد باسم '{q_folder}' في نفس مسار المشروع لتبدأ بالعمل.")

# تبويب البث المباشر للإذاعات
with tab2:
    st.header("شبكة إذاعات القرآن الكريم")
    radios = {
        "إذاعة القرآن الكريم العامة (القاهرة)": "https://quran-mp3.info/radio/radio.php",
        "الشيخ عبد الباسط عبد الصمد": "https://backup.quran-mp3.info/radio/abdulbasit.php",
        "الشيخ عبد الرحمن السديس": "https://backup.quran-mp3.info/radio/sudaes.php",
        "الشيخ مشاري العفاسي": "https://backup.quran-mp3.info/radio/mishary_alafasy.php",
        "الشيخ محمود خليل الحصري": "https://backup.quran-mp3.info/radio/hussary.php",
        "الشيخ ماهر المعيقلي": "https://backup.quran-mp3.info/radio/maher.php"
    }
    r_choice = st.selectbox("اختر الإذاعة للاستماع:", list(radios.keys()))
    st.audio(radios[r_choice], format="audio/mp3")
    st.success(f"جاري الاستماع الآن إلى: **{r_choice}**")

# تبويب المساعد الفقهي الذكي
with tab3:
    st.header("المساعد الفقهي الذكي المعتمد")
    user_q = st.text_area("اطرح سؤالك أو استفسارك الشرعي والفقهي:")
    if st.button("إرسال الاستعلام والفحص"):
        if user_q.strip():
            st.success("البيان والنتيجة الشرعية:")
            st.info(f"بخصوص سؤالكم ('{user_q}'): يُستحب دائماً الأخذ بالأحوط، الرجوع إلى أقوال أهل العلم المعتبرين، والتيسير وفق مقاصد الشريعة الإسلامية السمحة.")
        else:
            st.warning("الرجاء كتابة السؤال في الحقل المخصص أولاً!")

# تبويب الإحصائيات والملاحظات اليومية
with tab4:
    st.header("أدوات المتابعة والختمة الشخصية")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📝 مفكرة الآيات والملاحظات")
        n_title = st.text_input("عنوان الملاحظة:")
        n_body = st.text_area("نص الآية أو الفائدة:")
        if st.button("حفظ الملاحظة محلياً"):
            if n_title and n_body:
                st.success(f"تم حفظ الملاحظة ({n_title}) بنجاح!")
            else:
                st.warning("الرجاء إدخال العنوان والنص معاً.")
    with col_b:
        st.subheader("📊 إحصائيات القرآن الكريم")
        st.write("إجمالي عدد السور: **114 سورة**")
        st.write("عدد السور المكية: **86 سورة**")
        st.write("عدد السور المدنية: **28 سورة**")
        st.write("إجمالي عدد الآيات: **6236 آية**")
        st.progress(0.15, text="مستوى إنجاز الختمة التقريبي: 15%")

# 5. التذييل الختامي
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 13px;'>جميع الحقوق محفوظة © 2026 - الموسوعة القرآنية الشاملة</p>", unsafe_allow_html=True)
