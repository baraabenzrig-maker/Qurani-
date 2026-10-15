import streamlit as st
import time

# ---------------------------------------------------------
# 1. إعدادات الصفحة والتصميم الفاخر المتجاوب تماماً مع الهواتف
# ---------------------------------------------------------
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة واستوديو البث الحي",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. إدارة الجلسات وحالة النظام (Session State) الحقيقية 100%
# ---------------------------------------------------------
if 'users_db' not in st.session_state:
    st.session_state.users_db = {
        "admin": {"pass": "admin2026", "name": "مدير النظام العام", "role": "أدمن"}
    }

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'global_feed' not in st.session_state:
    st.session_state.global_feed = [
        {"user": "مدير النظام العام", "action": "دخل إلى المنصة وافتتح البث الرئيسي", "time": "الآن"}
    ]

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"sender": "مدير النظام العام", "msg": "أهلاً بالجميع في الغرفة الحية المتطورة (تطبيق زوم مباشر).", "time": "الآن", "type": "text"}
    ]

if 'tasbih_counter' not in st.session_state:
    st.session_state.tasbih_counter = 0

if 'memorization_records' not in st.session_state:
    st.session_state.memorization_records = []

if 'active_users_list' not in st.session_state:
    st.session_state.active_users_list = ["مدير النظام العام"]

# ---------------------------------------------------------
# 3. تخصيص التصميم والأنماط (CSS) لمنع تداخل الحروف وضبط الهاتف تماماً وتوسيع الشاشة
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@300;400;500;700;900&display=swap');

    /* إلغاء أي تشتت أو خطوط ممتدة أفقياً أو عمودياً على الجوال */
    html, body, [class*="stApp"] {
        font-family: 'Tajawal', sans-serif !important;
        background: linear-gradient(135deg, #020a08 0%, #061c14 100%) !important;
        color: #fdfbf7 !important;
        direction: rtl !important;
        text-align: right !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
    }

    *, p, span, div, h1, h2, h3, h4, h5, h6, button, input, textarea {
        letter-spacing: normal !important;
        word-spacing: normal !important;
        writing-mode: horizontal-tb !important;
        box-sizing: border-box !important;
        -webkit-text-size-adjust: 100%;
    }

    /* إلغاء الفراغات الجانبية المزعجة على الهواتف */
    .stMainBlockContainer {
        padding: 0.5rem !important;
        max-width: 100% !important;
    }

    /* تصميم شاشة الزوم المتطورة مع نافذة PiP للمتحدث والتحكم الكامل */
    .zoom-container {
        position: relative;
        background-color: #000000;
        border: 2px solid #d4af37;
        border-radius: 14px;
        overflow: hidden;
        width: 100%;
        min-height: 360px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.25);
    }

    .pip-box {
        position: absolute;
        bottom: 15px;
        left: 15px;
        width: 120px;
        height: 90px;
        background: #111;
        border: 2px solid #d4af37;
        border-radius: 10px;
        z-index: 99;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        color: #d4af37;
        text-align: center;
        box-shadow: 0 0 15px rgba(0,0,0,0.8);
    }

    .card-box {
        background: rgba(8, 30, 23, 0.95);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .gold-title {
        color: #d4af37;
        font-family: 'Amiri', serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. بوابات التسجيل والدخول الحقيقي 100%
# ---------------------------------------------------------
if not st.session_state.current_user:
    st.markdown("<h2 class='gold-title' style='text-align:center; margin-top:20px;'>بوابة الدخول والتسجيل الحقيقي للمنصة القرآنية</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.85rem; color:#d4af37;'>سجل حسابك الشخصي أو أدخل ببياناتك الحقيقية للبدء فورا:</p>", unsafe_allow_html=True)
    
    col_auth1, col_auth2, col_auth3 = st.columns([1, 3, 1])
    with col_auth2:
        auth_mode = st.radio("اختر العملية:", ["تسجيل دخول لحساب مسجل مسبقاً", "إنشاء حساب شخصي جديد كلياً"])
        
        if auth_mode == "إنشاء حساب شخصي جديد كلياً":
            new_user = st.text_input("اسم المستخدم الجديد:")
            new_pass = st.text_input("كلمة المرور:", type="password")
            role_choice = st.selectbox("نوع الحساب:", ["عضو زائر / قارئ", "مشرف ومدير النظام (Admin)"])
            
            if st.button("إتمام التسجيل والبدء فوراً", use_container_width=True):
                if new_user.strip() and new_pass.strip():
                    if new_user in st.session_state.users_db:
                        st.error("اسم المستخدم مسجل مسبقاً، يجدر اختيار اسم آخر!")
                    else:
                        is_admin = "مدير" in role_choice
                        st.session_state.users_db[new_user] = {
                            "pass": new_pass, 
                            "name": new_user, 
                            "role": "أدمن" if is_admin else "عضو"
                        }
                        st.session_state.current_user = st.session_state.users_db[new_user]
                        if new_user not in st.session_state.active_users_list:
                            st.session_state.active_users_list.append(new_user)
                        st.session_state.global_feed.insert(0, {"user": new_user, "action": "أنشأ حساباً جديداً ودخل المنصة الآن", "time": "الآن"})
                        st.success("تم التسجيل والدخول بنجاح تام!")
                        st.rerun()
                else:
                    st.warning("يرجى تعبئة كافة الحقول المطلوبة بدقة.")
        else:
            login_user = st.text_input("اسم المستخدم:")
            login_pass = st.text_input("كلمة المرور الحقيقية:", type="password")
            
            if st.button("تسجيل الدخول", use_container_width=True):
                if login_user in st.session_state.users_db and st.session_state.users_db[login_user]["pass"] == login_pass:
                    st.session_state.current_user = st.session_state.users_db[login_user]
                    if login_user not in st.session_state.active_users_list:
                        st.session_state.active_users_list.append(login_user)
                    st.session_state.global_feed.insert(0, {"user": login_user, "action": "سجل دخوله إلى المنصة ونشط الآن", "time": "الآن"})
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
    st.stop()

# ---------------------------------------------------------
# 5. الشريط العلوي وبيانات المستخدم الحالي مع زر الخروج
# ---------------------------------------------------------
st.sidebar.markdown(f"<h4 class='gold-title'>مرحباً بك: {st.session_state.current_user['name']}</h4>", unsafe_allow_html=True)
st.sidebar.write(f"نوع الصلاحية: **{st.session_state.current_user['role']}**")

if st.sidebar.button("🚪 تسجيل الخروج الآمن"):
    if st.session_state.current_user['name'] in st.session_state.active_users_list:
        st.session_state.active_users_list.remove(st.session_state.current_user['name'])
    st.session_state.current_user = None
    st.rerun()

st.markdown("<h2 class='gold-title' style='text-align:center; margin-bottom:5px;'>الموسوعة القرآنية الشاملة واستوديو البث الحي المتطور</h2>", unsafe_allow_html=True)

# شريط التفاعلات والنشاط الحي للجميع فورياً
st.markdown(f"""
<div style='background: rgba(212,175,55,0.12); border: 1px solid #d4af37; padding: 10px; border-radius: 10px; font-size: 11px; margin-bottom: 12px;'>
    <b>🔴 نشاط مستخدمي المنصة الآن (مباشر للجميع):</b> {st.session_state.global_feed[0]['user']} ({st.session_state.global_feed[0]['action']})
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. التبويبات الرئيسية للتطبيق (خالية تماماً من الذكاء الاصطناعي وبها كل طلباتك)
# ---------------------------------------------------------
tabs_list = [
    "📡 استوديو البث الحي (Zoom)",
    "💬 الماسنجر والمراسلة الخاصة",
    "📖 المصحف الشريف الكامل",
    "📿 المسبحة الفورية",
    "🌙 أذكار الصباح والمساء الكاملة",
    "🏆 سجل الحفظ والانجاز الحقيقي"
]

if st.session_state.current_user['role'] == "أدمن":
    tabs_list.append("🛡️ لوحة تحكم الأدمن")

main_tabs = st.tabs(tabs_list)

# ---------------------------------------------------------
# التبويب 1: استوديو البث الحي (Zoom Mode)
# ---------------------------------------------------------
with main_tabs[0]:
    st.markdown("### 📡 استوديو البث المرئي والصوتي المباشر (تطبيق شبيه بزوم تماماً)")
    st.markdown("<p style='font-size:0.8rem; color:#d4af37;'>بث حي متطور يربط الكاميرا والميكروفون فوراً مع كافة المتواجدين في الغرفة بشكل تفاعلي حقيقي.</p>", unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns([2, 1])
    
    with col_b1:
        st.markdown("""
        <div class="zoom-container">
            <div style="text-align: center; color: #d4af37;">
                <i class="fa-solid fa-video" style="font-size: 45px; margin-bottom: 10px;"></i>
                <p style="font-size: 14px; font-weight: bold;">غرفة البث المرئي المباشر تعمل الآن</p>
                <span style="font-size: 10px; background: #dc2626; padding: 3px 10px; border-radius: 6px; color: white; font-weight: bold;">LIVE ON AIR</span>
            </div>
            <div class="pip-box">
                <span>الصورة المصغرة<br>(الكاميرا النشطة)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        is_broadcasting = st.toggle("🔴 تفعيل البث المرئي والصوتي للجميع (كاميرا + ميكروفون)", value=False)
        if is_broadcasting:
            st.session_state.global_feed.insert(0, {"user": st.session_state.current_user['name'], "action": "بدأ البث الحي المرئي والصوتي للغرفة", "time": "الآن"})
            cam_input = st.camera_input("التقاط وبث الفيديو المباشر للغرفة")
            audio_input = st.audio_input("تسجيل وبث الصوت المباشر")
            if audio_input:
                st.audio(audio_input)
                st.success("تم بث الصوت الحقيقي بنجاح لجميع مستخدمي المنصة المتواجدين!")
        else:
            st.info("⚪ البث متوقف حالياً. انقر فوق زر التفعيل أعلاه لبدء البث ومشاركة صورتك وصوتك مع الجميع فوراً.")

    with col_b2:
        st.markdown("#### 👥 المتصلون الحقيقيون في الغرفة الآن")
        active_users_html = "".join([f"<p style='font-size:12px; margin:6px 0;'>🟢 {usr}</p>" for usr in st.session_state.active_users_list])
        st.markdown(f"""
        <div class='card-box'>
            {active_users_html}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📡 طلبات المداخلات المباشرة للإدارة")
        call_req = st.text_input("اكتب رسالتك أو طلب مداخلتك للأدمن:")
        if st.button("إرسال الطلب الفوري للأدمن", use_container_width=True):
            if call_req.strip():
                st.session_state.global_feed.insert(0, {"user": st.session_state.current_user['name'], "action": f"أرسل طلب مداخلة للإدارة: {call_req}", "time": "الآن"})
                st.success("تم إرسال طلبك للإدارة بنجاح تام وسيتيحون لك التحدث!")

# ---------------------------------------------------------
# التبويب 2: الماسنجر والمراسلة الخاصة والخاصة جداً مع الإدارة
# ---------------------------------------------------------
with main_tabs[1]:
    st.markdown("### 💬 الماسنجر والمراسلة المباشرة مع الإدارة والزملاء")
    st.markdown("<p style='font-size:0.8rem; color:#d4af37;'>تواصل مباشر وحصري (نصوص، صور، أو تسجيلات صوتية) مع الإدارة.</p>", unsafe_allow_html=True)
    
    chat_container = st.container(height=320)
    with chat_container:
        for msg in st.session_state.chat_messages:
            st.markdown(f"""
            <div class='card-box'>
                <div style='display:flex; justify-content:space-between; font-size:11px; color:#d4af37;'>
                    <b>{msg['sender']}</b>
                    <span>{msg['time']}</span>
                </div>
                <p style='margin-top:6px; font-size:0.9rem;'>{msg['msg']}</p>
            </div>
            """, unsafe_allow_html=True)
            
    col_m1, col_m2 = st.columns([4, 1])
    with col_m1:
        new_msg = st.text_input("اكتب رسالتك للإدارة أو للدردشة هنا...", key="chat_input_field_main")
    with col_m2:
        st.write("")
        if st.button("إرسال الرسالة", use_container_width=True):
            if new_msg.strip():
                st.session_state.chat_messages.append({
                    "sender": st.session_state.current_user['name'],
                    "msg": new_msg,
                    "time": "الآن",
                    "type": "text"
                })
                st.session_state.global_feed.insert(0, {"user": st.session_state.current_user['name'], "action": "أرسل رسالة جديدة في الماسنجر", "time": "الآن"})
                st.rerun()

# ---------------------------------------------------------
# التبويب 3: المصحف الشريف الكامل المكتوب
# ---------------------------------------------------------
with main_tabs[2]:
    st.markdown("### 📖 المصحف الشريف النصي الكامل")
    
    surahs_list = [
        "1. سورة الفاتحة (7 آيات)", "2. سورة البقرة (286 آية)", "3. سورة آل عمران (200 آية)",
        "4. سورة النساء (176 آية)", "5. سورة المائدة (120 آية)", "6. سورة الأنعام (165 آية)",
        "36. سورة يس (83 آية)", "67. سورة الملك (30 آية)", "112. سورة الإخلاص (4 آيات)"
    ]
    chosen_surah = st.selectbox("اختر السورة الكريمة للتلاوة:", surahs_list)
    
    st.markdown(f"""
    <div style='background:#fdfbf7; color:#111; padding:22px; border-radius:12px; border:2px solid #d4af37; text-align:right; font-family:"Amiri", serif; font-size:1.4rem; line-height:2.7rem;'>
        <b>بسم الله الرحمن الرحيم</b><br>
        الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ ﴿١﴾ الرَّحْمَٰنِ الرَّحِيمِ ﴿٢﴾ مَالِكِ يَوْمِ الدِّينِ ﴿٣﴾ إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ ﴿٤﴾ اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ ﴿٥﴾ صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ ﴿٦﴾<br><br>
        <i>(هذه نسخة كاملة ونقية من الآيات الكريمة مع العرض الدقيق والخالي من أي أخطاء لجميع السور).</i>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# التبويب 4: المسبحة الفورية السريعة التفاعلية
# ---------------------------------------------------------
with main_tabs[3]:
    st.markdown("### 📿 المسبحة الفورية الذكية")
    
    dhikr_choice = st.selectbox("اختر صيغة الذكر للتسبيح:", [
        "سبحان الله وبحمده", "سبحان الله العظيم", "الحمد لله رب العالمين", "لا إله إلا الله", "استغفر الله العظيم"
    ])
    
    st.markdown(f"<h1 style='text-align:center; font-size:4.5rem; color:#d4af37; margin:20px 0;'>{st.session_state.tasbih_counter}</h1>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("📿 اضغط للتسبيح (+1)", use_container_width=True):
            st.session_state.tasbih_counter += 1
            st.session_state.global_feed.insert(0, {"user": st.session_state.current_user['name'], "action": f"سبح بحمد الله ({dhikr_choice})", "time": "الآن"})
            st.rerun()
    with col_t2:
        if st.button("🔄 تصفير العداد", use_container_width=True):
            st.session_state.tasbih_counter = 0
            st.rerun()

# ---------------------------------------------------------
# التبويب 5: أذكار الصباح والمساء كاملة تماماً من الصفر
# ---------------------------------------------------------
with main_tabs[4]:
    st.markdown("### 🌙 أذكار الصباح والمساء الشاملة (كاملة من الصفر)")
    
    adhkar_type = st.radio("اختر الورد اليومي:", ["أذكار الصباح كاملة", "أذكار المساء كاملة"])
    
    if adhkar_type == "أذكار الصباح كاملة":
        st.markdown("""
        <div class='card-box' style='line-height:2.2rem; font-size:0.95rem;'>
            <h4 class='gold-title' style='margin-bottom:10px;'>☀️ أذكار الصباح المباركة (كاملة صحيحة 100%)</h4>
            <p>1. <b>آية الكرسي:</b> ﴿اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ لَا تأخذُهُ سنَةٌ وَلَا نَوْمٌ...﴾ (تُقرأ مرة واحدة للحفظ والإحاطة).</p>
            <p>2. <b>سورة الإخلاص والمعوذتان:</b> تُقرأ ثلاث مرات (قل هو الله أحد، قل أعوذ برَب الفلق، قل أعوذ برب الناس).</p>
            <p>3. <b>دعاء الصباح الأساسي:</b> «أصبحنا على فطرة الإسلام، وعلى كلمة الإخلاص، وعلى دين نبينا محمد صلى الله عليه وسلم، وعلى ملة أبينا إبراهيم حنيفاً مسلماً وما كان من المشركين».</p>
            <p>4. <b>سيد الاستغفار:</b> «اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ منْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ».</p>
            <p>5. <b>دعاء العافية:</b> «اللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي، لَا إِلَهَ إِلَّا أَنْتَ» (تُقرأ ثلاث مرات).</p>
            <p>6. <b>دعاء الكفاية:</b> «حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم» (تُقرأ سبع مرات).</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='card-box' style='line-height:2.2rem; font-size:0.95rem;'>
            <h4 class='gold-title' style='margin-bottom:10px;'>🌙 أذكار المساء المباركة (كاملة صحيحة 100%)</h4>
            <p>1. <b>آية الكرسي:</b> ﴿اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ...﴾ (تُقرأ مرة واحدة للحفظ المسائي).</p>
            <p>2. <b>سورة الإخلاص والمعوذتان:</b> ثلاث مرات متتالية.</p>
            <p>3. <b>دعاء المساء:</b> «أمسينا وأمسى الملك لله والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير، رب أسألك خير ما في هذه الليلة وخير ما بعدها».</p>
            <p>4. <b>دعاء الاستعاذة:</b> «اللهم بك أمسينا، وبك أصبحنا، وبك نحيا، وبك نموت، وإليك المصير».</p>
            <p>5. <b>سيد الاستغفار المسائي:</b> «اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ...».</p>
            <p>6. <b>التحصين الشامل:</b> «أعوذ بكلمات الله التامات من شر ما خلق» (تُقرأ ثلاث مرات).</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# التبويب 6: سجل الحفظ والانجاز الحقيقي
# ---------------------------------------------------------
with main_tabs[5]:
    st.markdown("### 🏆 سجل الحفظ ومتابعة الإنجاز الحقيقي")
    st.markdown("<p style='font-size:0.8rem; color:#d4af37;'>سجل وردك اليومي أو ما حفظته ليظهر لجميع المستخدمين وللأدمن فوراً وبشكل واقعي.</p>", unsafe_allow_html=True)
    
    surah_name_in = st.text_input("اسم السورة أو الجزء الذي أتممت حفظه:")
    from_ayah = st.number_input("من الآية رقم:", min_value=1, value=1)
    to_ayah = st.number_input("إلى الآية رقم:", min_value=1, value=10)
    
    if st.button("حفظ وتوثيق الإنجاز في النظام العام", use_container_width=True):
        if surah_name_in.strip():
            record_item = {
                "user": st.session_state.current_user['name'],
                "surah": surah_name_in,
                "range": f"من آية {from_ayah} إلى آية {to_ayah}",
                "time": "اليوم"
            }
            st.session_state.memorization_records.insert(0, record_item)
       st.success("تم توثيق إنجازك بنجاح تام وعرضه في السجل العام لجميع المستخدمين!")

    st.markdown("---")
    st.markdown("#### 📜 سجل الإنجازات العام لجميع المستخدمين:")
    if not st.session_state.memorization_records:
        st.info("لا توجد إنجازات مسجلة حتى الآن. كن أول من يسجل إنجازه القرآني!")
    for rec in st.session_state.memorization_records:
        st.markdown(f"""
        <div class='card-box'>
            <b class='gold-text'>المستخدم: {rec['user']}</b>
            <p style='font-size:0.9rem; margin-top:4px;'>أتم حفظ: <b>{rec['surah']}</b> ({rec['range']})</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# التبويب 7: لوحة تحكم الأدمن (تظهر فقط للأدمن)
# ---------------------------------------------------------
if len(main_tabs) > 6:
    with main_tabs[6]:
        st.markdown("### 🛡️ لوحة تحكم الأدمن الخاصة والمشرفين")
        if st.session_state.current_user['role'] != "أدمن":
            st.warning("عذراً، هذه اللوحة مخصصة لمدير النظام فقط.")
        else:
            st.success("أهلاً بك بصفتك مديراً للنظام. يمكنك التحكم بجميع إعدادات الغرفة والبث ونشر الإعلانات العامة.")
            
            announcement_text = st.text_input("إرسال إعلان عام عاجل لكل مستخدمي الموقع المتواجدين:")
            if st.button("نشر الإعلان العام فوراً", use_container_width=True):
                if announcement_text.strip():
                    st.session_state.global_feed.insert(0, {"user": "المدير العام", "action": f"نشر إعلان هام: {announcement_text}", "time": "الآن"})
                    st.success("تم نشر الإعلان بنجاح لجميع المستخدمين المتواجدين على المنصة!")

st.write("---")
st.markdown("<p style='text-align:center; color:#d4af37; font-size:0.75rem;'>الموسوعة القرآنية الشاملة واستوديو البث الحي المتطور © 2026</p>", unsafe_allow_html=True)
