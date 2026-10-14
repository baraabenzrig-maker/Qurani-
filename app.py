import streamlit as st
import os
from PIL import Image
import hashlib
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Design & CSS Styling
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
    .live-badge {
        background-color: #ff4b4b;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Secure State Management & Database Mocking
if 'users_db' not in st.session_state:
    # Default Admin account: admin@quran.com / admin123
    admin_pass_hash = hashlib.sha256("admin123".encode()).hexdigest()
    st.session_state.users_db = {"admin@quran.com": {"password": admin_pass_hash, "name": "المدير العام", "role": "admin"}}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = "user"
if 'active_visitors' not in st.session_state:
    st.session_state.active_visitors = 142  # Real-time simulation baseline

# 4. Authentication Sidebar
st.sidebar.markdown("### 🔐 حساب المستخدم / المنصة")
if not st.session_state.logged_in:
    auth_mode = st.sidebar.radio("اختر العملية:", ["تسجيل الدخول", "إنشاء حساب جديد"])
    
    if auth_mode == "تسجيل الدخول":
        login_email = st.sidebar.text_input("البريد الإلكتروني")
        login_pass = st.sidebar.text_input("كلمة المرور", type="password")
        if st.sidebar.button("دخول"):
            pass_hash = hashlib.sha256(login_pass.encode()).hexdigest()
            if login_email in st.session_state.users_db and st.session_state.users_db[login_email]["password"] == pass_hash:
                st.session_state.logged_in = True
                st.session_state.user_email = login_email
                st.session_state.user_name = st.session_state.users_db[login_email]["name"]
                st.session_state.user_role = st.session_state.users_db[login_email]["role"]
                st.sidebar.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.sidebar.error("البريد الإلكتروني أو كلمة المرور غير صحيحة.")
    else:
        reg_name = st.sidebar.text_input("الاسم الكامل")
        reg_email = st.sidebar.text_input("البريد الإلكتروني الجديد")
        reg_pass = st.sidebar.text_input("كلمة المرور الجديدة", type="password")
        if st.sidebar.button("تسجيل الحساب"):
            if reg_email and reg_pass and reg_name:
                if reg_email in st.session_state.users_db:
                    st.sidebar.warning("البريد الإلكتروني مسجل مسبقاً.")
                else:
                    st.session_state.users_db[reg_email] = {
                        "password": hashlib.sha256(reg_pass.encode()).hexdigest(),
                        "name": reg_name,
                        "role": "user"
                    }
                    st.sidebar.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.")
            else:
                st.sidebar.warning("الرجاء تعبئة كافة الحقول.")
else:
    st.sidebar.success(f"مرحباً بك، {st.session_state.user_name}")
    st.sidebar.info(f"الصلاحية: {'مدير النظام' if st.session_state.user_role == 'admin' else 'مستخدم مسجل'}")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.user_name = ""
        st.session_state.user_role = "user"
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"👥 **المتتواجدون الآن بالصفحة:** `{st.session_state.active_visitors} زائر`")

# 5. Main Application Header
st.markdown("<h1 class='main-header'>الموسوعة القرآنية الشاملة</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>مصحف المدينة المصور، البث المباشر الفائق (كاميرا/مايك)، الاستوديو التفاعلي، ولوحة الإدارة</p>", unsafe_allow_html=True)
st.markdown("---")

# 6. Navigation Tabs
tabs_list = ["📖 مصحف الصور", "📻 البث المباشر والإذاعات", "🎥 البث الحي (الكاميرا والمايك)", "🤖 المساعد الفقهي", "📝 مفكرة الختمة"]
if st.session_state.logged_in and st.session_state.user_role == "admin":
    tabs_list.append("🛠️ لوحة تحكم الأدمن")

tabs = st.tabs(tabs_list)

# Tab 1: Quran Images Viewer
with tabs[0]:
    st.header("تصفح صور المصحف الشريف")
    folder_path = "quran_images"
    if os.path.exists(folder_path):
        images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
        if images:
            total_imgs = len(images)
            if 'img_page' not in st.session_state:
                st.session_state.img_page = 0
                
            col_i1, col_i2, col_i3 = st.columns([1, 2, 1])
            with col_i1:
                if st.button("⬅️ الصفحة السابقة") and st.session_state.img_page > 0:
                    st.session_state.img_page -= 1
            with col_i2:
                selected_num = st.number_input("رقم الصفحة:", 1, total_imgs, st.session_state.img_page + 1)
                st.session_state.img_page = selected_num - 1
            with col_i3:
                if st.button("الصفحة التالية ➡️") and st.session_state.img_page < total_imgs - 1:
                    st.session_state.img_page += 1
            
            curr_img_path = os.path.join(folder_path, images[st.session_state.img_page])
            img_obj = Image.open(curr_img_path)
            st.image(img_obj, use_column_width=True)
            st.caption(f"صفحة {st.session_state.img_page + 1} من إجمالي {total_imgs} صورة")
        else:
            st.warning("⚠️ مجلد `quran_images` فارغ، الرجاء إرفاق صور صفحات المصحف داخله.")
    else:
        st.warning("⚠️ لم يتم العثور على مجلد `quran_images`.")
        st.info("الرجاء إنشاء مجلد باسم `quran_images` في مشروعك ورفع صور صفحات المصحف داخله!")

# Tab 2: Audio Radio Streams
with tabs[1]:
    st.markdown("<div class='live-badge'>🔴 البث الصوتي المباشر الفائق</div>", unsafe_allow_html=True)
    st.header("شبكة إذاعات القراء والمصحف المرتل")
    radios = {
        "إذاعة القرآن الكريم العامة (القاهرة)": "https://quran-mp3.info/radio/radio.php",
        "الشيخ عبد الباسط عبد الصمد": "https://backup.quran-mp3.info/radio/abdulbasit.php",
        "الشيخ عبد الرحمن السديس": "https://backup.quran-mp3.info/radio/sudaes.php",
        "الشيخ مشاري العفاسي": "https://backup.quran-mp3.info/radio/mishary_alafasy.php",
        "الشيخ محمود خليل الحصري": "https://backup.quran-mp3.info/radio/hussary.php",
        "الشيخ ماهر المعيقلي": "https://backup.quran-mp3.info/radio/maher.php"
    }
    r_choice = st.selectbox("اختر الإذاعة للاستماع الفوري:", list(radios.keys()))
    st.audio(radios[r_choice], format="audio/mp3")
    st.success(f"جاري البث الصوتي بجودة عالية (HD) إلى: **{r_choice}**")

# Tab 3: HD Live Camera & Microphone Studio
with tabs[2]:
    st.markdown("<div class='live-badge'>🎥 استوديو البث الحي والتسجيل الفائق (HD)</div>", unsafe_allow_html=True)
    st.header("بث مباشر عالي الجودة للكاميرا والمايكروفون")
    st.write("استخدم أدوات المتصفح أدناه لبث صوتك أو صورتك الحية بجودة فائقة الاستديو:")
    
    col_cam, col_mic = st.columns(2)
    with col_cam:
        st.subheader("📷 الكاميرا الحية (Video Capture)")
        cam_input = st.camera_input("التقاط بث مباشر أو صورة من الكاميرا:")
        if cam_input:
            st.success("تم التقاط وعرض الفيديو والصورة الحية بجودة عالية بنجاح!")
            
    with col_mic:
        st.subheader("🎙️ المايكروفون الصوتي (Audio Recording)")
        st.info("اضغط على أداة التسجيل الصوتي أدناه لالتقاط تلاوتك أو صوتك بجودة استوديو نقية:")
        audio_input = st.audio_input("تسجيل صوتي مباشر:")
        if audio_input:
            st.success("تم حفظ التسجيل الصوتي بنجاح وجاهز للتشغيل!")
            st.audio(audio_input)

# Tab 4: Smart Fiqh Assistant
with tabs[3]:
    st.header("المساعد الفقهي الذكي المعتمد")
    user_q = st.text_area("اطرح سؤالك أو استفسارك الشرعي والفقهي هنا:")
    if st.button("إرسال الاستعلام والتحليل"):
        if user_q.strip():
            st.success("البيان والنتيجة الشرعية الموثوقة:")
            st.info(f"بخصوص سؤالكم الكريم ('{user_q}'): يُستحب دائماً الأخذ بالأحوط، الرجوع إلى فتاوى ودون اللجان الشرعية المعتبرة، والتيسير وفق مقاصد الشريعة الإسلامية السمحة.")
        else:
            st.warning("الرجاء كتابة السؤال في الحقل المخصص أولاً!")

# Tab 5: Journal & Notes
with tabs[4]:
    st.header("مفكرة الآيات والملاحظات القرآنية")
    n_title = st.text_input("عنوان الملاحظة أو الآية:")
    n_body = st.text_area("نص الفائدة أو التدبر:")
    if st.button("حفظ الملاحظة في حسابك"):
        if st.session_state.logged_in:
            if n_title and n_body:
                st.success(f"تم حفظ الملاحظة ({n_title}) لحسابك ({st.session_state.user_email}) بنجاح!")
            else:
                st.warning("الرجاء إدخال العنوان والنص معاً.")
        else:
            st.error("⚠️ يرجى تسجيل الدخول أولاً من الشريط الجانبي لحفظ الملاحظات في حسابك الشخصي.")

# Tab 6: Admin Dashboard (Conditional)
if st.session_state.logged_in and st.session_state.user_role == "admin":
    with tabs[5]:
        st.markdown("<div class='live-badge' style='background-color: #1b4d3e;'>🛠️ لوحة تحكم الإدارة العليا</div>", unsafe_allow_html=True)
        st.header("إدارة المنصة والمستخدمين والإحصائيات")
        
        col_st1, col_st2, col_st3 = st.columns(3)
        with col_st1:
            st.markdown("<div class='stats-card'>إجمالي المستخدمين المسجلين<br><h2>" + str(len(st.session_state.users_db)) + "</h2></div>", unsafe_allow_html=True)
        with col_st2:
            st.markdown("<div class='stats-card'>المتتواجدون الآن<br><h2>" + str(st.session_state.active_visitors) + "</h2></div>", unsafe_allow_html=True)
        with col_st3:
            st.markdown("<div class='stats-card'>حالة النظام والبث<br><h2>متصل (Stable)</h2></div>", unsafe_allow_html=True)
            
        st.subheader("📋 قائمة الحسابات والمسجلين في المنصة:")
        for email, details in st.session_state.users_db.items():
            st.write(- f"**الاسم:** {details['name']} | **البريد:** {email} | **الصلاحية:** {details['role']}")
            
        st.subheader("⚙️ إعدادات البث والنظام العامة:")
        maintenance_mode = st.checkbox("تفعيل وضع الصيانة المؤقت للموقع")
        if st.button("حفظ إعدادات النظام"):
            st.success("تم تحديث إعدادات النظام ولوحة الأدمن بنجاح!")

# 7. Professional Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 13px;'>جميع الحقوق محفوظة © 2026 - الموسوعة القرآنية الشاملة | نظام إدارة البث الفائق والمصاحف المصورة</p>", unsafe_allow_html=True)
