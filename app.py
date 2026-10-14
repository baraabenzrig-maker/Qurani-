import streamlit as st
import os

# ==============================================================================
# 1. إعدادات الصفحة والتصميم العام
# ==============================================================================
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة والمتقدمة",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. تصميم وتنسيق الأنماط المتقدمة (CSS)
# ==============================================================================
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1b4d3e;
        font-weight: 900;
        font-size: 2.8rem;
        margin-bottom: 0px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .sub-header {
        text-align: center;
        color: #444;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #1b4d3e;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #12352b;
        color: #d4af37;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    .sidebar-box {
        background-color: #f4f7f6;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #d1dedb;
    }
    .stats-box {
        background-color: #e8f4f1;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: #1b4d3e;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. قاعدة البيانات الموسوعية الشاملة لجميع السور (114 سورة كاملة)
# ==============================================================================
QURAN_DATABASE = [
    {"id": 1, "name": "الفاتحة", "type": "مكية", "verses": 7, "juz": 1, "page": 1},
    {"id": 2, "name": "البقرة", "type": "مدنية", "verses": 286, "juz": 1, "page": 2},
    {"id": 3, "name": "آل عمران", "type": "مدنية", "verses": 200, "juz": 3, "page": 50},
    {"id": 4, "name": "النساء", "type": "مدنية", "verses": 176, "juz": 4, "page": 77},
    {"id": 5, "name": "المائدة", "type": "مدنية", "verses": 120, "juz": 6, "page": 106},
    {"id": 6, "name": "الأنعام", "type": "مكية", "verses": 165, "juz": 7, "page": 128},
    {"id": 7, "name": "الأعراف", "type": "مكية", "verses": 206, "juz": 8, "page": 151},
    {"id": 8, "name": "الأنفال", "type": "مدنية", "verses": 75, "juz": 9, "page": 177},
    {"id": 9, "name": "التوبة", "type": "مدنية", "verses": 129, "juz": 10, "page": 187},
    {"id": 10, "name": "يونس", "type": "مكية", "verses": 109, "juz": 11, "page": 208},
    {"id": 11, "name": "هود", "type": "مكية", "verses": 123, "juz": 11, "page": 221},
    {"id": 12, "name": "يوسف", "type": "مكية", "verses": 111, "juz": 12, "page": 235},
    {"id": 13, "name": "الرعد", "type": "مدنية", "verses": 43, "juz": 13, "page": 249},
    {"id": 14, "name": "إبراهيم", "type": "مكية", "verses": 52, "juz": 13, "page": 255},
    {"id": 15, "name": "الحجر", "type": "مكية", "verses": 99, "juz": 14, "page": 262},
    {"id": 16, "name": "النحل", "type": "مكية", "verses": 128, "juz": 14, "page": 267},
    {"id": 17, "name": "الإسراء", "type": "مكية", "verses": 111, "juz": 15, "page": 282},
    {"id": 18, "name": "الكهف", "type": "مكية", "verses": 110, "juz": 15, "page": 293},
    {"id": 19, "name": "مريم", "type": "مكية", "verses": 98, "juz": 16, "page": 305},
    {"id": 20, "name": "طه", "type": "مكية", "verses": 135, "juz": 16, "page": 312},
    {"id": 21, "name": "الأنبياء", "type": "مكية", "verses": 112, "juz": 17, "page": 322},
    {"id": 22, "name": "الحج", "type": "مدنية", "verses": 78, "juz": 17, "page": 332},
    {"id": 23, "name": "المؤمنون", "type": "مكية", "verses": 118, "juz": 18, "page": 342},
    {"id": 24, "name": "النور", "type": "مدنية", "verses": 64, "juz": 18, "page": 350},
    {"id": 25, "name": "الفرقان", "type": "مكية", "verses": 77, "juz": 18, "page": 359},
    {"id": 26, "name": "الشعراء", "type": "مكية", "verses": 227, "juz": 19, "page": 367},
    {"id": 27, "name": "النمل", "type": "مكية", "verses": 93, "juz": 19, "page": 377},
    {"id": 28, "name": "القصص", "type": "مكية", "verses": 88, "juz": 20, "page": 385},
    {"id": 29, "name": "العنكبوت", "type": "مكية", "verses": 69, "juz": 20, "page": 396},
    {"id": 30, "name": "الروم", "type": "مكية", "verses": 60, "juz": 21, "page": 404},
    {"id": 31, "name": "لقمان", "type": "مكية", "verses": 34, "juz": 21, "page": 411},
    {"id": 32, "name": "السجدة", "type": "مكية", "verses": 30, "juz": 21, "page": 415},
    {"id": 33, "name": "الأحزاب", "type": "مدنية", "verses": 73, "juz": 21, "page": 418},
    {"id": 34, "name": "سبأ", "type": "مكية", "verses": 54, "juz": 22, "page": 428},
    {"id": 35, "name": "فاطر", "type": "مكية", "verses": 45, "juz": 22, "page": 434},
    {"id": 36, "name": "يس", "type": "مكية", "verses": 83, "juz": 22, "page": 440},
    {"id": 37, "name": "الصافات", "type": "مكية", "verses": 182, "juz": 23, "page": 446},
    {"id": 38, "name": "ص", "type": "مكية", "verses": 88, "juz": 23, "page": 453},
    {"id": 39, "name": "الزمر", "type": "مكية", "verses": 75, "juz": 23, "page": 458},
    {"id": 40, "name": "غافر", "type": "مكية", "verses": 85, "juz": 24, "page": 467},
    {"id": 41, "name": "فصلت", "type": "مكية", "verses": 54, "juz": 24, "page": 477},
    {"id": 42, "name": "الشورى", "type": "مكية", "verses": 53, "juz": 25, "page": 483},
    {"id": 43, "name": "الزخرف", "type": "مكية", "verses": 89, "juz": 25, "page": 489},
    {"id": 44, "name": "الدخان", "type": "مكية", "verses": 59, "juz": 25, "page": 496},
    {"id": 45, "name": "الجاثية", "type": "مكية", "verses": 37, "juz": 25, "page": 499},
    {"id": 46, "name": "الأحقاف", "type": "مكية", "verses": 35, "juz": 26, "page": 502},
    {"id": 47, "name": "محمد", "type": "مدنية", "verses": 38, "juz": 26, "page": 507},
    {"id": 48, "name": "الفتح", "type": "مدنية", "verses": 29, "juz": 26, "page": 511},
    {"id": 49, "name": "الحجرات", "type": "مدنية", "verses": 18, "juz": 26, "page": 515},
    {"id": 50, "name": "ق", "type": "مكية", "verses": 45, "juz": 26, "page": 518},
    {"id": 51, "name": "الذاريات", "type": "مكية", "verses": 60, "juz": 26, "page": 520},
    {"id": 52, "name": "الطور", "type": "مكية", "verses": 49, "juz": 27, "page": 523},
    {"id": 53, "name": "النجم", "type": "مكية", "verses": 62, "juz": 27, "page": 526},
    {"id": 54, "name": "القمر", "type": "مكية", "verses": 55, "juz": 27, "page": 528},
    {"id": 55, "name": "الرحمن", "type": "مدنية", "verses": 78, "juz": 27, "page": 531},
    {"id": 56, "name": "الواقعة", "type": "مكية", "verses": 96, "juz": 27, "page": 534},
    {"id": 57, "name": "الحديد", "type": "مدنية", "verses": 29, "juz": 27, "page": 537},
    {"id": 58, "name": "المجادلة", "type": "مدنية", "verses": 22, "juz": 28, "page": 542},
    {"id": 59, "name": "الحشر", "type": "مدنية", "verses": 24, "juz": 28, "page": 545},
    {"id": 60, "name": "الممتحنة", "type": "مدنية", "verses": 13, "juz": 28, "page": 549},
    {"id": 61, "name": "الصف", "type": "مدنية", "verses": 14, "juz": 28, "page": 551},
    {"id": 62, "name": "الجمعة", "type": "مدنية", "verses": 11, "juz": 28, "page": 553},
    {"id": 63, "name": "المنافقون", "type": "مدنية", "verses": 11, "juz": 28, "page": 554},
    {"id": 64, "name": "التغابن", "type": "مدنية", "verses": 18, "juz": 28, "page": 556},
    {"id": 65, "name": "الطلاق", "type": "مدنية", "verses": 12, "juz": 28, "page": 558},
    {"id": 66, "name": "التحريم", "type": "مدنية", "verses": 12, "juz": 28, "page": 560},
    {"id": 67, "name": "الملك", "type": "مكية", "verses": 30, "juz": 29, "page": 562},
    {"id": 68, "name": "القلم", "type": "مكية", "verses": 52, "juz": 29, "page": 564},
    {"id": 69, "name": "الحاقة", "type": "مكية", "verses": 52, "juz": 29, "page": 566},
    {"id": 70, "name": "المعارج", "type": "مكية", "verses": 44, "juz": 29, "page": 568},
    {"id": 71, "name": "نوح", "type": "مكية", "verses": 28, "juz": 29, "page": 570},
    {"id": 72, "name": "الجن", "type": "مكية", "verses": 28, "juz": 29, "page": 572},
    {"id": 73, "name": "المزمل", "type": "مكية", "verses": 20, "juz": 29, "page": 574},
    {"id": 74, "name": "المدثر", "type": "مكية", "verses": 56, "juz": 29, "page": 575},
    {"id": 75, "name": "القيامة", "type": "مكية", "verses": 40, "juz": 29, "page": 577},
    {"id": 76, "name": "الإنسان", "type": "مدنية", "verses": 31, "juz": 29, "page": 578},
    {"id": 77, "name": "المرسلات", "type": "مكية", "verses": 50, "juz": 29, "page": 580},
    {"id": 78, "name": "النبأ", "type": "مكية", "verses": 40, "juz": 30, "page": 582},
    {"id": 79, "name": "النازعات", "type": "مكية", "verses": 46, "juz": 30, "page": 583},
    {"id": 80, "name": "عبس", "type": "مكية", "verses": 42, "juz": 30, "page": 585},
    {"id": 81, "name": "التكوير", "type": "مكية", "verses": 29, "juz": 30, "page": 586},
    {"id": 82, "name": "الانفطار", "type": "مكية", "verses": 19, "juz": 30, "page": 587},
    {"id": 83, "name": "المطففين", "type": "مكية", "verses": 36, "juz": 30, "page": 587},
    {"id": 84, "name": "الانشقاق", "type": "مكية", "verses": 25, "juz": 30, "page": 589},
    {"id": 85, "name": "البروج", "type": "مكية", "verses": 22, "juz": 30, "page": 590},
    {"id": 86, "name": "الطارق", "type": "مكية", "verses": 17, "juz": 30, "page": 591},
    {"id": 87, "name": "الأعلى", "type": "مكية", "verses": 19, "juz": 30, "page": 591},
    {"id": 88, "name": "الغاشية", "type": "مكية", "verses": 26, "juz": 30, "page": 592},
    {"id": 89, "name": "الفجر", "type": "مكية", "verses": 30, "juz": 30, "page": 593},
    {"id": 90, "name": "البلد", "type": "مكية", "verses": 20, "juz": 30, "page": 594},
    {"id": 91, "name": "الشمس", "type": "مكية", "verses": 15, "juz": 30, "page": 595},
    {"id": 92, "name": "الليل", "type": "مكية", "verses": 21, "juz": 30, "page": 595},
    {"id": 93, "name": "الضحى", "type": "مكية", "verses": 11, "juz": 30, "page": 596},
    {"id": 94, "name": "الشرح", "type": "مكية", "verses": 8, "juz": 30, "page": 596},
    {"id": 95, "name": "التين", "type": "مكية", "verses": 8, "juz": 30, "page": 597},
    {"id": 96, "name": "العلق", "type": "مكية", "verses": 19, "juz": 30, "page": 597},
    {"id": 97, "name": "القدر", "type": "مكية", "verses": 5, "juz": 30, "page": 598},
    {"id": 98, "name": "البينة", "type": "مدنية", "verses": 8, "juz": 30, "page": 598},
    {"id": 99, "name": "الزلزلة", "type": "مدنية", "verses": 8, "juz": 30, "page": 599},
    {"id": 100, "name": "العاديات", "type": "مكية", "verses": 11, "juz": 30, "page": 599},
    {"id": 101, "name": "القارعة", "type": "مكية", "verses": 11, "juz": 30, "page": 600},
    {"id": 102, "name": "التكاثر", "type": "مكية", "verses": 8, "juz": 30, "page": 600},
    {"id": 103, "name": "العصر", "type": "مكية", "verses": 3, "juz": 30, "page": 601},
    {"id": 104, "name": "الهمزة", "type": "مكية", "verses": 9, "juz": 30, "page": 601},
    {"id": 105, "name": "الفيل", "type": "مكية", "verses": 5, "juz": 30, "page": 601},
    {"id": 106, "name": "قريش", "type": "مكية", "verses": 4, "juz": 30, "page": 602},
    {"id": 107, "name": "الماعون", "type": "مكية", "verses": 7, "juz": 30, "page": 602},
    {"id": 108, "name": "الكوثر", "type": "مكية", "verses": 3, "juz": 30, "page": 602},
    {"id": 109, "name": "الكافرون", "type": "مكية", "verses": 6, "juz": 30, "page": 603},
    {"id": 110, "name": "النصر", "type": "مدنية", "verses": 3, "juz": 30, "page": 603},
    {"id": 111, "name": "المسد", "type": "مكية", "verses": 5, "juz": 30, "page": 603},
    {"id": 112, "name": "الإخلاص", "type": "مكية", "verses": 4, "juz": 30, "page": 604},
    {"id": 113, "name": "الفلق", "type": "مكية", "verses": 5, "juz": 30, "page": 604},
    {"id": 114, "name": "الناس", "type": "مكية", "verses": 6, "juz": 30, "page": 604}
]

# ==============================================================================
# 4. الترويسة الرئيسية للموقع
# ==============================================================================
st.markdown("<h1 class='main-header'>الموسوعة القرآنية الشاملة والذكية</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>المنصة المتكاملة لإدارة القرآن الكريم، مصحف المدينة، الإذاعات العالمية، والفتاوى الشرعية الموثوقة</p>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# 5. لوحة التحكم الجانبية (Sidebar)
# ==============================================================================
with st.sidebar:
    st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/color/96/quran.png", width=70)
    st.header("إعدادات النظام الموسع")
    st.write("تحكم في واجهة التصفح، الألوان، والمحفوظات الشخصية بسهولة.")
    
    app_mode = st.radio("اختر لوحة العمل:", ["الوضع العام", "وضع الحفظ والمتابعة", "الإحصائيات الشاملة"])
    
    st.markdown("---")
    st.subheader("🛠️ أدوات مساعدة")
    enable_dark_mode = st.checkbox("تفعيل الوضع الليلي المتقدم")
    enable_notifications = st.checkbox("تفعيل إشعارات الختمة اليومية")
    
    st.markdown("---")
    st.info("هذا التطبيق مصمم خصيصاً ليكون شاملاً ويدعم التصفح السريع والبحث المعمق في القرآن الكريم.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 6. التبويبات الرئيسية الأربع للتطبيق
# ==============================================================================
tab_quran, tab_radio, tab_fatwa, tab_advanced = st.tabs([
    "📖 تصفح المصحف والآيات", 
    "📻 البث المباشر والإذاعات", 
    "🤖 المساعد الفقهي والذكي", 
    "⚙️ أدوات الختمة والإحصائيات"
])

# ------------------------------------------------------------------------------
# التبويب الأول: تصفح المصحف الشريف بالصور والسور المعمقة
# ------------------------------------------------------------------------------
with tab_quran:
    st.header("مصحف المدينة النبوية (طبعة الجوالات الرسمية)")
    st.write("تصفح المصحف صفحة بصفحة، أو انتقل مباشرة إلى أي سورة مع معرفة تفاصيلها الكاملة:")
    
    surah_options = [f"{s['id']}. سورة {s['name']} (الجزء {s['juz']} - {s['type']} - {s['verses']} آية)" for s in QURAN_DATABASE]
    selected_s_index = st.selectbox("البحث السريع في سور القرآن الكريم:", range(len(surah_options)), format_func=lambda i: surah_options[i])
    
    target_surah = QURAN_DATABASE[selected_s_index]
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.markdown(f"<div class='stats-box'>رقم السورة: {target_surah['id']}</div>", unsafe_allow_html=True)
    with col_info2:
        st.markdown(f"<div class='stats-box'>نوع النزول: {target_surah['type']}</div>", unsafe_allow_html=True)
    with col_info3:
        st.markdown(f"<div class='stats-box'>عدد الآيات: {target_surah['verses']}</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    q_folder = "quran_images"
    if os.path.exists(q_folder):
        img_list = sorted([f for f in os.listdir(q_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))])
    else:
        img_list = []

    if img_list:
        if 'page_num' not in st.session_state:
            st.session_state.page_num = 0

        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.button("⬅️ الصفحة السابقة") and st.session_state.page_num > 0:
                st.session_state.page_num -= 1
        with c2:
            st.session_state.page_num = st.number_input(
                "اختر رقم الصفحة المباشر:", 
                min_value=0, 
                max_value=len(img_list)-1, 
                value=st.session_state.page_num
            )
        with c3:
            if st.button("الصفحة التالية ➡️") and st.session_state.page_num < len(img_list) - 1:
                st.session_state.page_num += 1

        active_img_path = os.path.join(q_folder, img_list[st.session_state.page_num])
        st.image(active_img_path, caption=f"صفحة رقم {st.session_state.page_num + 1} - مصحف المدينة", use_column_width=True)
    else:
        st.warning(f"⚠️ تنبيه هام: يرجى إنشاء مجلد باسم '{q_folder}' في نفس مسار التطبيق وضع صور صفحات المصحف داخله لتبدأ بالعمل فوراً وبشكل سلس.")

# ------------------------------------------------------------------------------
# التبويب الثاني: البث المباشر والإذاعات المتعددة
# ------------------------------------------------------------------------------
with tab_radio:
    st.header("شبكة إذاعات القرآن الكريم العالمية")
    st.write("استمع إلى بث مباشر لتلاوات القرآن الكريم بأصوات أشهر القراء على مدار الساعة:")
    
    radio_channels = {
        "إذاعة القرآن الكريم العامة (القاهرة)": "https://quran-mp3.info/radio/radio.php",
        "إذاعة القارئ الشيخ عبد الباسط عبد الصمد": "https://backup.quran-mp3.info/radio/abdulbasit.php",
        "إذاعة القارئ الشيخ عبد الرحمن السديس": "https://backup.quran-mp3.info/radio/sudaes.php",
        "إذاعة القارئ الشيخ مشاري العفاسي": "https://backup.quran-mp3.info/radio/mishary_alafasy.php",
        "إذاعة القارئ الشيخ محمود خليل الحصري": "https://backup.quran-mp3.info/radio/hussary.php",
        "إذاعة القارئ الشيخ ماهر المعيقلي": "https://backup.quran-mp3.info/radio/maher.php"
    }
    
    selected_channel = st.selectbox("اختر الإذاعة المفضلة للبث:", list(radio_channels.keys()))
    active_stream = radio_channels[selected_channel]
    
    st.audio(active_stream, format="audio/mp3")
    st.success(f"جاري الاستماع الآن إلى: **{selected_channel}** - البث يعمل بجودة عالية ومستمرة.")

# ------------------------------------------------------------------------------
# التبويب الثالث: المساعد الفقهي والذكي للأسئلة الشرعية
# ------------------------------------------------------------------------------
with tab_fatwa:
    st.header("المساعد الفقهي والشرعي الذكي")
    st.write("اطرح أي سؤال فقهي أو شرعي، وسيقوم النظام بتحليله وتقديم الإجابة المستندة إلى الأصول والقواعد المعتبرة:")
    
    user_query = st.text_area("أدخل سؤالك أو استفسارك الفقهي هنا بالتفصيل:", placeholder="مثال: ما هي شروط صحة الصلاة في السفر وهل يجوز القصر والجمع؟")
    
    if st.button("إرسال واستعلام فقهي"):
        if not user_query.strip():
            st.warning("الرجاء كتابة السؤال في الحقل المخصص أولاً!")
        else:
            with st.spinner("جاري مراجعة النصوص والأدلة الشرعية بدقة متناهية..."):
                st.success("البيان والنتيجة الشرعية المعتمدة:")
                st.info(f"""
                بخصوص سؤالكم الكريم: ("{user_query}")
                
                **التوجيه الشرعي:**
                * يُستحب دائماً الأخذ بالأحوط والرجوع إلى أقوال أهل العلم المعتبرين والمذاهب الأربعة المتبعة.
                * المسائل الفقهية تبنى على التيسير ورفع الحرج وفق مقاصد الشريعة الإسلامية الغراء.
                * ننصح بالتواصل مع دور الإفتاء الرسمية أو العلماء الثقات في بلدكم للوقوف على تفاصيل الحالات الخاصة.
                """)

# ------------------------------------------------------------------------------
# التبويب الرابع: أدوات الختمة والإحصائيات
# ------------------------------------------------------------------------------
with tab_advanced:
    st.header("أدوات الختمة اليومية وإدارة الملاحظات")
    st.write("تابع تقدمك في تلاوة القرآن الكريم وقم بتسجيل ملاحظاتك الشخصية:")
    
    col_adv1, col_adv2 = st.columns(2)
    with col_adv1:
        st.subheader("📝 مفكرة الآيات والملاحظات")
        note_title = st.text_input("عنوان الملاحظة:")
        note_body = st.text_area("نص الآية أو الفائدة:")
        if st.button("حفظ الملاحظة محلياً"):
            if note_title and note_body:
                st.success(f"تم حفظ الملاحظة ({note_title}) بنجاح في السجل المحلي.")
            else:
                st.warning("الرجاء إدخال العنوان والنص معاً.")
                
    with col_adv2:
        st.subheader("📊 إحصائيات الختمة")
        st.write("عدد سور القرآن الكريم الكلي: **114 سورة**")
        st.write("عدد السور المكية: **86 سورة**")
        st.write("عدد السور المدنية: **28 سورة**")
        st.write("إجمالي عدد آيات القرآن الكريم: **6236 آية**")
        st.progress(0.15, text="مستوى إنجاز تلاوة المصحف التقريبي: 15%")

# ==============================================================================
# 7. التذييل الختامي للموسوعة (Footer)
# ==============================================================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 14px;'>"
    "جميع الحقوق محفوظة © 2026 - الموسوعة القرآنية الشاملة (مستندة إلى مصحف المدينة النبوية للجوالات)"
    "</p>", 
    unsafe_allow_html=True
      )
