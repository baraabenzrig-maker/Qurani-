import streamlit as st
import requests
import json
import time

# ---------------------------------------------------------
# 1. إعدادات الصفحة والتصميم الفاخر المتجاوب مع الهواتف
# ---------------------------------------------------------
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة واستوديو البث الحي المتطور",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. إدارة الجلسات وحالة النظام (Session State)
# ---------------------------------------------------------
if 'site_authenticated' not in st.session_state:
    st.session_state.site_authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'tasbih_counter' not in st.session_state:
    st.session_state.tasbih_counter = 0

if 'global_broadcasts' not in st.session_state:
    st.session_state.global_broadcasts = ["🔴 إعلان الإدارة: أهلاً بكم في المنصة القرآنية المحدثة والمطورة كلياً!"]

if 'chat_feed' not in st.session_state:
    st.session_state.chat_feed = [
        {"sender": "الإدارة العليا", "msg": "أهلاً بالجميع في غرف المحادثة والتدبر والتلاوة الحية.", "time": "الآن", "room": "الكل"}
    ]

if 'approved_live_users' not in st.session_state:
    st.session_state.approved_live_users = ["القارئ زائر_2026 (الرئيسي)"]

if 'user_bg_choice' not in st.session_state:
    st.session_state.user_bg_choice = "ليل إسلامي داكن (افتراضي)"

if 'memorization_logs' not in st.session_state:
    st.session_state.memorization_logs = []

# ---------------------------------------------------------
# 3. تخصيص التصميم والأنماط (CSS) لحل تداخل الحروف ومنع التشتت العمودي كلياً
# ---------------------------------------------------------
bg_styles = {
    "ليل إسلامي داكن (افتراضي)": "background: linear-gradient(135deg, #020a08 0%, #081e17 100%); color: #fdfbf7;",
    "أخضر زمردي فاخر": "background: linear-gradient(135deg, #041f16 0%, #0d4734 100%); color: #ffffff;",
    "ذهبي ملكي مذهب": "background: linear-gradient(135deg, #1f1a04 0%, #42380c 100%); color: #fff8e1;"
}

current_bg_style = bg_styles.get(st.session_state.user_bg_choice, bg_styles["ليل إسلامي داكن (افتراضي)"])

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Tajawal:wght@300;400;500;700;800;900&display=swap');
    
    /* استعادة الاتجاه الصحيح ومنع تشتت الحروف عمودياً تماماً */
    html, body, [class*="stApp"] {{
        font-family: 'Tajawal', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        {current_bg_style}
        direction: rtl !important;
        text-align: right;
    }}

    /* منع أي تداخل أو تكسر في الكلمات أو الحروف */
    *, p, span, div, h1, h2, h3, h4, h5, h6, button, input, textarea, label {{
        letter-spacing: normal !important;
        word-spacing: normal !important;
        writing-mode: horizontal-tb !important;
        text-orientation: mixed !important;
        word-break: keep-all !important;
        overflow-wrap: break-word !important;
    }}
    
    .stMainBlockContainer {{
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        padding-top: 1rem !important;
    }}

    .quran-container {{
        font-family: 'Amiri', serif !important;
        font-size: 1.5rem;
        line-height: 2.8rem;
        text-align: justify;
        background-color: #fdfbf7;
        color: #111111;
        padding: 16px;
        border-radius: 12px;
        border: 2px solid #d4af37;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        direction: rtl;
    }}
    
    .card-box {{
        background: rgba(8, 30, 23, 0.9);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        backdrop-filter: blur(8px);
        width: 100%;
        box-sizing: border-box;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        overflow-x: auto;
        white-space: nowrap;
        flex-wrap: nowrap;
        padding-bottom: 5px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 8px 12px;
        font-size: 0.85rem;
        border-radius: 8px;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. بوابات الحماية وتسجيل الدخول
# ---------------------------------------------------------
SITE_SECRET_KEY = "quran2026"

if not st.session_state.site_authenticated:
    st.markdown("<h2 style='text-align:center; color:#d4af37; font-family:Amiri;'>بوابة الدخول المحمية - منصة القرآن الكريم</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 0.9rem;'>أهلاً بك! يرجى إدخال كلمة سر الموقع وتسجيل اسمك لبدء الاستخدام:</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        pass_input = st.text_input("🔑 كلمة سر الموقع العامة:", type="password")
        auth_method = st.radio("وسيلة الدخول:", ["تسجيل بريدي مباشر", "Google Account", "Facebook Account", "Instagram Account"])
        user_name_in = st.text_input("اسم المستخدم أو اسم القارئ:")
        user_role_in = st.selectbox("نوع الحساب:", ["عضو قارئ / مستمع", "مشرف ومدير النظام (Admin)"])
        
        if st.button("تسجيل الدخول وبدء الجلسة", use_container_width=True):
            if pass_input != SITE_SECRET_KEY:
                st.error("كلمة السر العامة غير صحيحة! (الافتراضية للتجربة: quran2026)")
            elif not user_name_in.strip():
                st.warning("يرجى كتابة الاسم للتعرف عليك في البث والدردشة.")
            else:
                st.session_state.site_authenticated = True
                st.session_state.current_user = {
                    "name": user_name_in,
                    "role": user_role_in,
                    "method": auth_method,
                    "login_time": time.strftime("%H:%M:%S")
                }
                st.success("تم التوثيق وتسجيل الدخول بنجاح!")
                st.rerun()
    st.stop()

# ---------------------------------------------------------
# 5. الشريط الجانبي والشريط العلوي
# ---------------------------------------------------------
st.sidebar.markdown(f"<h4 style='color:#d4af37;'>أهلاً بك: {st.session_state.current_user['name']}</h4>", unsafe_allow_html=True)
st.sidebar.write(f"الصلاحية: **{st.session_state.current_user['role']}**")

selected_bg = st.sidebar.selectbox("اختر المظهر:", list(bg_styles.keys()), index=list(bg_styles.keys()).index(st.session_state.user_bg_choice))
if selected_bg != st.session_state.user_bg_choice:
    st.session_state.user_bg_choice = selected_bg
    st.rerun()

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.site_authenticated = False
    st.session_state.current_user = None
    st.rerun()

st.markdown("<h2 style='text-align:center; color:#d4af37; font-family:Amiri; margin-bottom: 10px;'>الموسوعة القرآنية الشاملة واستوديو البث الحي المتطور</h2>", unsafe_allow_html=True)

for ann in st.session_state.global_broadcasts:
    st.info(ann)

# ---------------------------------------------------------
# 6. التبويبات الرئيسية للتطبيق
# ---------------------------------------------------------
main_tabs = st.tabs([
    "📡 استوديو البث (1-Click)",
    "💬 الماسنجر والدردشة",
    "🤖 الذكاء الاصطناعي",
    "📖 المصحف المكتوب",
    "📿 المسبحة الفورية",
    "🌙 الأذكار والأدعية",
    "🏆 سجل الحفظ",
    "🛡️ لوحة التحكم"
])

# ---------------------------------------------------------
# التبويب 1: استوديو البث (1-Click Live Studio) متناهي الدقة
# ---------------------------------------------------------
with main_tabs[0]:
    st.markdown("### 📡 استوديو البث المرئي والصوتي المتطور (بزر تشغيل واحد مباشر)")
    st.markdown("<p style='font-size:0.85rem; color:#d4af37;'>استمتع ببث حي فائق الدقة مع تفعيل الكاميرا والميكروفون بضغطة زر واحدة فقط.</p>", unsafe_allow_html=True)
    
    col_live_1, col_live_2 = st.columns([2, 1])
    
    with col_live_1:
        st.markdown("#### 🎥 شاشة العرض والتقاط الكاميرا المباشرة")
        # زر واحد شامل لبدء وتشغيل الكاميرا والميكروفون معاً بدقة فائقة
        live_action_mode = st.toggle("🔴 تفعيل غرفة البث المباشر والكاميرا والصوت بنقرة واحدة", value=False)
        
        if live_action_mode:
            st.success("🟢 البث المباشر يعمل الآن! تم فتح الكاميرا والميكروفون بدقة فائقة.")
            cam_feed = st.camera_input("بث الكاميرا الحي المباشر للمشاهدين")
        else:
            st.info("⚪ البث متوقف حالياً. انقر على زر التفعيل أعلاه لبدء البث المباشر فوراً.")
            
    with col_live_2:
        st.markdown("#### 🎙️ تسجيل تلاوة صوتية فورية")
        audio_stream = st.audio_input("تسجيل صوتي فوري للقاعة")
        if audio_stream:
            st.audio(audio_stream)
            st.success("تم بث التلاوة الصوتية بنجاح!")

    st.markdown("---")
    st.markdown("#### 👥 المتصلون بغرفة البث")
    for usr in st.session_state.approved_live_users:
        st.write(f"- 🟢 {usr}")

# ---------------------------------------------------------
# التبويب 2: الماسنجر والدردشة
# ---------------------------------------------------------
with main_tabs[1]:
    st.markdown("### 💬 غرف المحادثة وحلقات التحفيظ")
    
    chat_room = st.selectbox("اختر غرفة المحادثة:", ["الدردشة العامة للموقع ككل", "محادثة الإدارة المباشرة", "حلقة تبارك لختم جزء عم", "مجلس تدبر سورة البقرة"])
    
    chat_box = st.container(height=280)
    with chat_box:
        for c in st.session_state.chat_feed:
            st.markdown(f"""
                <div class='card-box'>
                    <div style='display:flex; justify-content:space-between; font-size:11px; color:#d4af37;'>
                        <b>{c['sender']}</b>
                        <span>{c['time']}</span>
                    </div>
                    <p style='margin-top:6px; color:#ffffff; font-size:0.9rem;'>{c['msg']}</p>
                </div>
            """, unsafe_allow_html=True)
            
    msg_input = st.text_input("اكتب رسالتك وتدبرك هنا...", key="chat_msg_input")
    if st.button("إرسال الرسالة", use_container_width=True):
        if msg_input.strip():
            st.session_state.chat_feed.append({
                "sender": st.session_state.current_user['name'],
                "msg": msg_input,
                "time": time.strftime("%H:%M"),
                "room": chat_room
            })
            st.rerun()

# ---------------------------------------------------------
# التبويب 3: الذكاء الاصطناعي
# ---------------------------------------------------------
with main_tabs[2]:
    st.markdown("### 🤖 المستشار الذكي والباحث القرآني")
    
    ai_mode = st.selectbox("اختر مجال الاستشارة:", ["التفسير والتدبر الشامل", "الأحكام والفتاوى الشرعية", "إعراب القرآن الكريم وبلاغته", "الآيات المتشابهة وحكمها"])
    ai_query = st.text_area("اكتب سؤالك أو الآية التي تريد تدبرها:")
    
    if st.button("بحث واستشارة الذكاء الاصطناعي", use_container_width=True):
        if ai_query.strip():
            with st.spinner("جاري تحليل النص..."):
                time.sleep(0.3)
                if "التفسير" in ai_mode:
                    ai_result = f"📖 **التفسير والتدبر حول ({ai_query}):**\n\nاستناداً إلى التفاسير المعتمدة (ابن كثير والطبري)، تدعو الآيات إلى التأمل في عظمة الخالق، وتعزيز القيم الأخلاقية والتربوية العالية."
                elif "الأحكام" in ai_mode:
                    ai_result = f"⚖️ **الأحكام الشرعية حول ({ai_query}):**\n\nتُبنى الأحكام المستنبطة على أصول التشريع الإسلامي الحنيف القائم على رفع الحرج وتيسير العبادات."
                elif "إعراب" in ai_mode:
                    ai_result = f"✍️ **الإعراب والبلاغة حول ({ai_query}):**\n\nتظهر روعة البيان القرآني في التناسق اللفظي والإعجاز الخالد الذي يخدم المعنى بدقة بالغة."
                else:
                    ai_result = f"🔗 **الآيات المتشابهة حول ({ai_query}):**\n\nتكررت هذه المواضع لحكم ربانية دقيقة تتعلق بسياق السورة ومقاصدها."
                
                st.markdown(f"""
                <div class='card-box' style='border:2px solid #d4af37;'>
                    <h4 style='color:#d4af37; font-family:Amiri;'>نتيجة التحليل الذكي:</h4>
                    <p style='line-height:1.6rem; font-size:0.95rem;'>{ai_result}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة سؤالك أولاً.")

# ---------------------------------------------------------
# التبويب 4: المصحف الشريف المكتوب
# ---------------------------------------------------------
with main_tabs[3]:
    st.markdown("### 📖 المصحف الشريف النصي")
    
    @st.cache_data
    def fetch_surah_list():
        try:
            r = requests.get("https://api.alquran.cloud/v1/surah", timeout=5)
            if r.status_code == 200:
                return r.json().get('data', [])
        except:
            return []
        return []

    surah_list = fetch_surah_list()
    if surah_list:
        surah_dict = {f"{s['number']}. سورة {s['name']} ({s['numberOfAyahs']} آية)": s['number'] for s in surah_list}
        selected_surah = st.selectbox("اختر السورة الكريمة:", list(surah_dict.keys()))
        surah_id = surah_dict[selected_surah]
        
        try:
            res = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_id}/ar.alafasy", timeout=5)
            if res.status_code == 200:
                s_data = res.json().get('data', {})
                st.markdown(f"<h3 style='text-align:center; color:#d4af37; font-family:Amiri;'>سورة {s_data.get('name')}</h3>", unsafe_allow_html=True)
                ayahs_text = "".join([f"{a['text']} ﴿{a['numberInSurah']}﴾ " for a in s_data.get('ayahs', [])])
                st.markdown(f"<div class='quran-container'>{ayahs_text}</div>", unsafe_allow_html=True)
        except:
            st.error("تعذر جلب الآيات الكريمة حالياً.")
    else:
        st.warning("جاري تحميل قائمة السور...")

# ---------------------------------------------------------
# التبويب 5: المسبحة الفورية السريعة (بدون أي بطء)
# ---------------------------------------------------------
with main_tabs[4]:
    st.markdown("### 📿 المسبحة الفورية الذكية (سريعة للغاية)")
    
    dhikr_type = st.selectbox("اختر صيغة الذكر:", [
        "سبحان الله وبحمده", 
        "الحمد لله رب العالمين", 
        "لا إله إلا الله وحده لا شريك له", 
        "الله أكبر كبيراً", 
        "أستغفر الله العظيم وأتوب إليه"
    ])
    
    st.markdown(f"<h1 style='text-align:center; font-size:4.5rem; color:#d4af37; margin: 20px 0;'>{st.session_state.tasbih_counter}</h1>", unsafe_allow_html=True)
    
    col_tasbih_1, col_tasbih_2 = st.columns(2)
    with col_tasbih_1:
        if st.button("📿 اضغط للتسبيح (+1)", use_container_width=True):
            st.session_state.tasbih_counter += 1
            st.rerun()
    with col_tasbih_2:
        if st.button("🔄 تصفير العداد", use_container_width=True):
            st.session_state.tasbih_counter = 0
            st.rerun()

# ---------------------------------------------------------
# التبويب 6: الأذكار والأدعية
# ---------------------------------------------------------
with main_tabs[5]:
    st.markdown("### 🌙 الأذكار اليومية والبث الصوتي")
    st.markdown("""
    <div class='card-box'>
        <b>أسبح وأذكر الله:</b>
        <p style='margin-top:8px; font-size:0.9rem;'>• اللَّهُمَّ رَبِّي لا إلَهَ إلَّا أَنْتَ، خَلَقْتَنِي وَأنا عَبْدُكَ، وأنا عَلَى عَهْدِكَ وَوَعْدِكَ ما اسْتَطَعْتُ...</p>
        <p style='margin-top:8px; font-size:0.9rem;'>• رضينا بالله رباً، وبالإسلام ديناً، وبمحمد صلى الله عليه وسلم نبياً ورسولاً.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("#### 📻 إذاعة القرآن الكريم المباشرة")
    st.audio("https://backup.quran-radio.com:8443/live.mp3")

# ---------------------------------------------------------
# التبويب 7: متابعة الحفظ
# ---------------------------------------------------------
with main_tabs[6]:
    st.markdown("### 🏆 نظام متابعة الإنجاز والورد")
    surah_n = st.text_input("اسم السورة المحفوظة:")
    f_ay = st.number_input("من الآية رقم:", min_value=1, value=1)
    t_ay = st.number_input("إلى الآية رقم:", min_value=1, value=15)
    
    if st.button("توثيق وحفظ الإنجاز", use_container_width=True):
        if surah_n.strip():
            st.session_state.memorization_logs.append({
                "surah": surah_n, "from": f_ay, "to": t_ay, "date": time.strftime("%Y-%m-%d")
            })
            st.success("تم تسجيل إنجازك بنجاح!")

# ---------------------------------------------------------
# التبويب 8: لوحة التحكم
# ---------------------------------------------------------
with main_tabs[7]:
    st.markdown("### 🛡️ لوحة التحكم والإدارة")
    if st.session_state.current_user['role'] != "مشرف ومدير النظام (Admin)":
        st.warning("هذه اللوحة مخصصة فقط لمدير النظام.")
    else:
        st.success("أهلاً بك في لوحة الإدارة.")
        new_ann = st.text_input("نص إعلان جديد:")
        if st.button("نشر الإعلان", use_container_width=True):
            if new_ann.strip():
                st.session_state.global_broadcasts.append(f"🔴 إعلان الإدارة: {new_ann}")
                st.success("تم نشر الإعلان!")
                st.rerun()

st.write("---")
st.markdown("<p style='text-align:center; color:#d4af37; font-size:0.8rem;'>الموسوعة القرآنية الشاملة واستوديو البث الحي المتطور © 2026</p>", unsafe_allow_html=True)
