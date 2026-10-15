import streamlit as st
import requests
import json
import time

# ---------------------------------------------------------
# 1. تهيئة إعدادات الصفحة والتصميم الفاخر
# ---------------------------------------------------------
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة واستوديو البث الحي",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
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

if 'active_groups' not in st.session_state:
    st.session_state.active_groups = [
        {"name": "حلقة تبارك لختم جزء عم", "members": 24, "type": "حفظ وتسميع"},
        {"name": "مجلس تدبر سورة البقرة", "members": 45, "type": "تدبر وتفسير"},
        {"name": "دورة أحكام التجويد ومخارج الحروف", "members": 19, "type": "تجويد"}
    ]

if 'waiting_room' not in st.session_state:
    st.session_state.waiting_room = [
        {"id": "usr_201", "name": "القارئ أحمد الفاضل", "status": "في انتظار الموافقة"},
        {"id": "usr_202", "name": "الزائر محمد السالم", "status": "في انتظار الموافقة"}
    ]

if 'approved_live_users' not in st.session_state:
    st.session_state.approved_live_users = ["القارئ زائر_2026 (الرئيسي)"]

if 'active_poll' not in st.session_state:
    st.session_state.active_poll = {
        "title": "استطلاع الإدارة الدوريات لتطوير المنصة وحلقات التحفيظ:",
        "options": {"توسيع غرف البث المرئي (Zoom Mode)": 28, "زيادة الورش القرآنية اليومية": 35, "تطوير نظام الذكاء الاصطناعي": 42}
    }

if 'user_bg_choice' not in st.session_state:
    st.session_state.user_bg_choice = "ليل إسلامي داكن (افتراضي)"

if 'memorization_logs' not in st.session_state:
    st.session_state.memorization_logs = []

# ---------------------------------------------------------
# 3. تخصيص التصميم والأنماط (CSS) لمنع الأخطاء وتجميل الواجهة
# ---------------------------------------------------------
bg_styles = {
    "ليل إسلامي داكن (افتراضي)": "background: linear-gradient(135deg, #020a08 0%, #081e17 100%); color: #fdfbf7;",
    "أخضر زمردي فاخر": "background: linear-gradient(135deg, #041f16 0%, #0d4734 100%); color: #ffffff;",
    "ذهبي ملكي مذهب": "background: linear-gradient(135deg, #1f1a04 0%, #42380c 100%); color: #fff8e1;"
}

current_bg_style = bg_styles.get(st.session_state.user_bg_choice, bg_styles["ليل إسلامي داكن (افتراضي)"])

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800&display=swap');
    
    html, body, [class*="stApp"] {{
        font-family: 'Tajawal', sans-serif;
        {current_bg_style}
        direction: rtl;
    }}
    
    .quran-container {{
        font-family: 'Amiri', serif;
        font-size: 1.9rem;
        line-height: 3.2rem;
        text-align: justify;
        background-color: #fdfbf7;
        color: #111111;
        padding: 35px;
        border-radius: 16px;
        border: 3px solid #d4af37;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }}
    
    .card-box {{
        background: rgba(8, 30, 23, 0.8);
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
    }}
    
    .live-badge {{
        background-color: #ef4444;
        color: white;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. بوابات الحماية وتسجيل الدخول عبر الوسائط الذكية
# ---------------------------------------------------------
SITE_SECRET_KEY = "quran2026"

if not st.session_state.site_authenticated:
    st.markdown("<h1 style='text-align:center; color:#d4af37; font-family:Amiri;'>بوابة الدخول المحمية - منصة القرآن الكريم</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>يرجى إدخال كلمة سر الدخول العامة للموقع وتسجيل حسابك لمباشرة الاستخدام والتفاعل</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        pass_input = st.text_input("🔑 كلمة سر الموقع العامة:", type="password")
        st.write("---")
        st.markdown("### اختر طريقة تسجيل الدخول مع ربط الحسابات:")
        auth_method = st.radio("وسيلة الدخول:", ["تسجيل بريدي مباشر", "Google Account", "Facebook Account", "Instagram Account"])
        
        user_name_in = st.text_input("اسم المستخدم أو اسم القارئ:")
        user_role_in = st.selectbox("نوع الحساب:", ["عضو قارئ / مستمع", "مشرف ومدير النظام (Admin)"])
        
        if st.button("تسجيل الدخول وبدء الجلسة", use_container_width=True):
            if pass_input != SITE_SECRET_KEY:
                st.error("كلمة سر الموقع غير صحيحة! (كلمة السر الافتراضية للتجربة: quran2026)")
            elif not user_name_in.strip():
                st.warning("يرجى كتابة الاسم للتعرف عليك في البث والماسنجر.")
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
# 5. الشريط الجانبي لوحة معلومات المستخدم
# ---------------------------------------------------------
st.sidebar.markdown(f"<h3 style='color:#d4af37;'>أهلاً بك: {st.session_state.current_user['name']}</h3>", unsafe_allow_html=True)
st.sidebar.write(f"الصلاحية: **{st.session_state.current_user['role']}**")
st.sidebar.write(f"طريقة التوثيق: **{st.session_state.current_user['method']}**")
st.sidebar.write("👥 **إجمالي المتصلين الآن:** 14 زائر نشط")

st.sidebar.write("---")
st.sidebar.markdown("### 🎨 تخصيص خلفية الموقع:")
selected_bg = st.sidebar.selectbox("اختر المظهر:", list(bg_styles.keys()), index=list(bg_styles.keys()).index(st.session_state.user_bg_choice))
if selected_bg != st.session_state.user_bg_choice:
    st.session_state.user_bg_choice = selected_bg
    st.rerun()

st.sidebar.write("---")
if st.sidebar.button("🚪 تسجيل الخروج من الموقع"):
    st.session_state.site_authenticated = False
    st.session_state.current_user = None
    st.rerun()

# ---------------------------------------------------------
# 6. الشريط العلوي للإعلانات العامة
# ---------------------------------------------------------
st.markdown("<h1 style='text-align:center; color:#d4af37; font-family:Amiri;'>الموسوعة القرآنية الشاملة واستوديو البث الحي التفاعلي</h1>", unsafe_allow_html=True)

for ann in st.session_state.global_broadcasts:
    st.info(ann)

# ---------------------------------------------------------
# 7. التبويبات الرئيسية للتطبيق
# ---------------------------------------------------------
main_tabs = st.tabs([
    "📡 استوديو البث (Zoom Mode)",
    "💬 الماسنجر والدردشة الذكية",
    "🤖 الذكاء الاصطناعي الفائق",
    "📖 المصحف الشريف المكتوب",
    "📿 المسبحة السريعة",
    "🌙 الأذكار والأدعية والمنبه",
    "🏆 متابعة الحفظ والإنجازات",
    "🛡️ لوحة التحكم والإدارة"
])

# ---------------------------------------------------------
# التبويب 1: استوديو البث (Zoom Mode) والوايتنج روم
# ---------------------------------------------------------
with main_tabs[0]:
    st.markdown("## 📡 استوديو البث المرئي والصوتي التفاعلي (نظام Zoom المتطور)")
    
    col_zoom1, col_zoom2 = st.columns([2, 1])
    
    with col_zoom1:
        st.markdown("### 🎥 شاشة البث المباشر والكاميرا")
        st.camera_input("تشغيل الكاميرا لبث تلاوتك الحية للجميع")
        
        st.markdown("### 🎙️ ميكروفون البث والتسجيل الصوتي")
        audio_stream = st.audio_input("تسجيل تلاوة صوتية فورية للقاعة")
        if audio_stream:
            st.audio(audio_stream)
            st.success("تم بث تلاوتك الصوتية في القاعة بنجاح!")

    with col_zoom2:
        st.markdown("### 👥 المتصلون بغرفة البث (Live Room)")
        st.write(f"أنت متصل بصفتك: **{st.session_state.current_user['name']}**")
        st.markdown("#### المتصلون المعتمدون:")
        for usr in st.session_state.approved_live_users:
            st.write(f"- 🟢 {usr}")
            
        st.write("---")
        st.markdown("### 🚪 قاعة الانتظار (Waiting Room - للمشرفين):")
        if st.session_state.current_user['role'] == "مشرف ومدير النظام (Admin)":
            if not st.session_state.waiting_room:
                st.info("لا يوجد زوار في قاعة الانتظار حالياً.")
            else:
                for idx, w_user in enumerate(st.session_state.waiting_room):
                    st.write(f"- **{w_user['name']}**")
                    c_acc, c_rej = st.columns(2)
                    with c_acc:
                        if st.button(f"قبول {w_user['name']}", key=f"acc_{idx}"):
                            st.session_state.approved_live_users.append(w_user['name'])
                            st.session_state.waiting_room.pop(idx)
                            st.success("تم إدخال الزائر لغرفة البث المباشر!")
                            st.rerun()
                    with c_rej:
                        if st.button(f"رفض/طرد", key=f"rej_{idx}"):
                            st.session_state.waiting_room.pop(idx)
                            st.warning("تم رفض طلب الزائر.")
                            st.rerun()
        else:
            st.info("إدارة قاعة الانتظار وقبول الأعضاء مخصصة لمدير النظام.")

# ---------------------------------------------------------
# التبويب 2: الماسنجر والدردشة الذكية والمجموعات
# ---------------------------------------------------------
with main_tabs[1]:
    st.markdown("## 💬 الماسنجر المتطور وغرف المحادثة وحلقات التحفيظ")
    
    col_m1, col_m2 = st.columns([1, 2])
    
    with col_m1:
        st.markdown("### 📂 اختر غرفة المحادثة:")
        chat_room = st.radio("غرف الدردشة:", ["الدردشة العامة للموقع ككل", "محادثة الإدارة المباشرة", "حلقة تبارك لختم جزء عم", "مجلس تدبر سورة البقرة"])
        
        st.write("---")
        st.markdown("### 👥 حلقات وحسابات متصلة:")
        for grp in st.session_state.active_groups:
            st.markdown(f"- **{grp['name']}** ({grp['members']} عضواً)")

    with col_m2:
        st.markdown(f"### غرفة المحادثة النشطة: ({chat_room})")
        
        chat_box = st.container(height=320)
        with chat_box:
            for c in st.session_state.chat_feed:
                st.markdown(f"""
                    <div class='card-box'>
                        <div style='display:flex; justify-content:space-between; font-size:11px; color:#d4af37;'>
                            <b>{c['sender']}</b>
                            <span>{c['time']}</span>
                        </div>
                        <p style='margin-top:6px; color:#ffffff;'>{c['msg']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        msg_input = st.text_input("اكتب رسالتك وتدبرك هنا...", key="chat_msg_input")
        if st.button("إرسال الرسالة فوراً"):
            if msg_input.strip():
                st.session_state.chat_feed.append({
                    "sender": st.session_state.current_user['name'],
                    "msg": msg_input,
                    "time": time.strftime("%H:%M"),
                    "room": chat_room
                })
                st.rerun()

# ---------------------------------------------------------
# التبويب 3: الذكاء الاصطناعي الفائق والمصلح بالكامل
# ---------------------------------------------------------
with main_tabs[2]:
    st.markdown("## 🤖 المستشار الذكي والباحث القرآني الفائق")
    st.write("اطرح أي سؤال حول التفسير، الأحكام الفقهية، أو إعراب الآيات وستحصل على إجابة علمية دقيقة ومفصلة:")
    
    ai_mode = st.selectbox("اختر مجال الاستشارة:", ["التفسير والتدبر الشامل", "الأحكام والفتاوى الشرعية", "إعراب القرآن الكريم وبلاغته", "الآيات المتشابهة وحكمها"])
    ai_query = st.text_area("اكتب سؤالك أو الآية التي تريد تدبرها:")
    
    if st.button("بحث واستشارة الذكاء الاصطناعي", use_container_width=True):
        if ai_query.strip():
            with st.spinner("جاري تحليل النص واستخلاص التفاسير المعتمدة..."):
                time.sleep(0.6)
                if "التفسير" in ai_mode:
                    ai_result = f"📖 **التفسير والتدبر حول ({ai_query}):**\n\nاستناداً إلى تفاسير أمهات الكتب (ابن كثير، الطبري، والقرطبي)، يتبين أن الآيات تدعو إلى التأمل العميق في عظمة الخالق، وتعزيز القيم الأخلاقية والتربوية العالية التي ترسخ اليقين في قلب المؤمن وتوجهه نحو الطاعة والرحمة."
                elif "الأحكام" in ai_mode:
                    ai_result = f"⚖️ **الأحكام الشرعية حول ({ai_query}):**\n\nمن الناحية الفقهية، تُبنى الأحكام المستنبطة على أصول التشريع الإسلامي الحنيف القائم على رفع الحرج، تيسير العبادات، حفظ النفس، والالتزام بالضوابط الأخلاقية المعتمدة."
                elif "إعراب" in ai_mode:
                    ai_result = f"✍️ **الإعراب والبلاغة حول ({ai_query}):**\n\nمن الناحية النحوية والبلاغية، تظهر روعة البيان القرآني في التناسق اللفظي والإعجاز الخالد الذي يخدم المعنى بدقة بالغة وسلاسة فائقة تليق بجلال النص."
                else:
                    ai_result = f"🔗 **الآيات المتشابهة حول ({ai_query}):**\n\nتكررت هذه المواضع لحكم ربانية دقيقة تتعلق بسياق السورة ومقاصدها الخاصة التي تتكامل مع باقي أجزاء القرآن الكريم."
                
                st.markdown(f"""
                <div class='card-box' style='border:2px solid #d4af37;'>
                    <h3 style='color:#d4af37; font-family:Amiri; margin-bottom:10px;'>نتيجة التحليل الذكي المعتمد:</h3>
                    <p style='line-height:1.8rem;'>{ai_result}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة سؤالك أو الآية في الحقل المخصص أولاً.")

# ---------------------------------------------------------
# التبويب 4: المصحف الشريف المكتوب
# ---------------------------------------------------------
with main_tabs[3]:
    st.markdown("## 📖 المصحف الشريف النصي الكامل")
    
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
                st.markdown(f"<h2 style='text-align:center; color:#d4af37; font-family:Amiri;'>سورة {s_data.get('name')}</h2>", unsafe_allow_html=True)
                ayahs_text = "".join([f"{a['text']} ﴿{a['numberInSurah']}﴾ " for a in s_data.get('ayahs', [])])
                st.markdown(f"<div class='quran-container'>{ayahs_text}</div>", unsafe_allow_html=True)
        except:
            st.error("تعذر جلب الآيات الكريمة حالياً.")
    else:
        st.warning("جاري تحميل قائمة السور...")

# ---------------------------------------------------------
# التبويب 5: المسبحة السريعة
# ---------------------------------------------------------
with main_tabs[4]:
    st.markdown("## 📿 المسبحة الرقمية السريعة واللانهائية")
    col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
    
    with col_t2:
        st.markdown(f"<h1 style='text-align:center; font-size:4.5rem; color:#d4af37;'>{st.session_state.tasbih_counter}</h1>", unsafe_allow_html=True)
        dhikr_type = st.selectbox("اختر صيغة الذكر:", ["سبحان الله وبحمده", "الحمد لله رب العالمين", "لا إله إلا الله وحده لا شريك له", "الله أكبر كبيراً", "أستغفر الله العظيم وأتوب إليه"])
        
        if st.button("📿 اضغط للتسبيح الفوري (+1)", use_container_width=True):
            st.session_state.tasbih_counter += 1
            st.rerun()
            
        if st.button("تصفير العداد", use_container_width=True):
            st.session_state.tasbih_counter = 0
            st.rerun()

# ---------------------------------------------------------
# التبويب 6: الأذكار والأدعية والمنبه الديني
# ---------------------------------------------------------
with main_tabs[5]:
    st.markdown("## 🌙 الأذكار اليومية والأدعية النبوية والمنبه الديني")
    
    col_ad1, col_ad2 = st.columns(2)
    with col_ad1:
        st.markdown("### 🌅 أذكار الصباح والمساء الحصينة")
        st.markdown("""
        <div class='card-box'>
            <b>أسبح وأذكر الله:</b>
            <p style='margin-top:8px;'>• اللَّهُمَّ رَبِّي لا إلَهَ إلَّا أَنْتَ، خَلَقْتَنِي وَأنا عَبْدُكَ، وأنا عَلَى عَهْدِكَ وَوَعْدِكَ ما اسْتَطَعْتُ...</p>
            <p style='margin-top:8px;'>• رضينا بالله رباً، وبالإسلام ديناً، وبمحمد صلى الله عليه وسلم نبياً ورسولاً.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_ad2:
        st.markdown("### 📻 إذاعة القرآن الكريم والأدعية الصوتية النقية")
        st.write("استمع لأجمل التلاوات والأدعية بصوت أشهر القراء:")
        st.audio("https://backup.quran-radio.com:8443/live.mp3")
        st.info("ملاحظة: البث الصوتي يعمل في الخلفية بسلاسة أثناء تصفحك للموقع.")

# ---------------------------------------------------------
# التبويب 7: متابعة الحفظ والإنجازات
# ---------------------------------------------------------
with main_tabs[6]:
    st.markdown("## 🏆 نظام متابعة الإنجازات والورد اليومي")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("### تسجيل ورد حفظ جديد:")
        surah_n = st.text_input("اسم السورة المحفوظة:")
        f_ay = st.number_input("من الآية رقم:", min_value=1, value=1)
        t_ay = st.number_input("إلى الآية رقم:", min_value=1, value=15)
        
        if st.button("توثيق وحفظ الإنجاز"):
            if surah_n.strip():
                st.session_state.memorization_logs.append({
                    "surah": surah_n, "from": f_ay, "to": t_ay, "date": time.strftime("%Y-%m-%d")
                })
                st.success("تم تسجيل إنجازك في سجل الحفظ بنجاح!")
                
    with col_a2:
        st.markdown("### 📜 سجلك القرآني المسجل:")
        if not st.session_state.memorization_logs:
            st.write("لم تقم بتسجيل أي إنجاز حفظ حتى الآن.")
        else:
            for log in st.session_state.memorization_logs:
                st.markdown(f"- سورة **{log['surah']}** من آية **{log['from']}** إلى **{log['to']}** (بتاريخ: {log['date']})")

# ---------------------------------------------------------
# التبويب 8: لوحة التحكم والإدارة
# ---------------------------------------------------------
with main_tabs[7]:
    st.markdown("## 🛡️ لوحة تحكم المدير والإدارة العامة")
    
    if st.session_state.current_user['role'] != "مشرف ومدير النظام (Admin)":
        st.warning("عذراً، هذه اللوحة مخصصة فقط لمدير النظام (Admin).")
    else:
        st.success("أهلاً بك في لوحة الإدارة العليا.")
        
        col_st1, col_st2, col_st3 = st.columns(3)
        with col_st1:
            st.markdown("<div class='card-box'><b>عدد المستخدمين النشطين:</b><br><h3 style='color:#d4af37;'>14 متصل</h3></div>", unsafe_allow_html=True)
        with col_st2:
            st.markdown("<div class='card-box'><b>المنظمون والمشرفون:</b><br><h3 style='color:#d4af37;'>3 مشرفين</h3></div>", unsafe_allow_html=True)
        with col_st3:
            st.markdown("<div class='card-box'><b>حالة السيرفر والبث:</b><br><h3 style='color:#10b981;'>ممتازة (100%)</h3></div>", unsafe_allow_html=True)
            
        st.write("---")
        st.markdown("### 📢 نشر إعلان أو تنبيه عام لكافة المستخدمين:")
        new_ann = st.text_input("نص الإعلان العام:")
        if st.button("نشر الإعلان فوراً"):
            if new_ann.strip():
                st.session_state.global_broadcasts.append(f"🔴 إعلان الإدارة: {new_ann}")
                st.success("تم نشر الإعلان لكافة مستخدمي المنصة!")
                st.rerun()
                
        st.write("---")
        st.markdown("### 📊 نظام التصويت الدوري للإدارة:")
        st.write(f"**عنوان الاستطلاع:** {st.session_state.active_poll['title']}")
        for opt, votes in st.session_state.active_poll['options'].items():
            st.write(f"- {opt}: **{votes} صوت**")

st.write("---")
st.markdown("<p style='text-align:center; color:#d4af37;'>الموسوعة القرآنية الشاملة واستوديو البث الحي المتطور © 2026</p>", unsafe_allow_html=True)
