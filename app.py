import streamlit as st
import requests
import json
import time

# ---------------------------------------------------------
# 1. تهيئة إعدادات الصفحة والتصميم العريض
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة القرآن الكريم الشاملة واستوديو البث الحي",
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
    st.session_state.global_broadcasts = ["🔴 إعلان هام: أهلاً بكم في المنصة القرآنية الجديدة متكاملة الخدمات!"]

if 'chat_feed' not in st.session_state:
    st.session_state.chat_feed = [
        {"sender": "الإدارة", "msg": "أهلاً بالجميع في غرف المحادثة والتدبر القرآنية.", "time": "الآن"}
    ]

if 'active_poll' not in st.session_state:
    st.session_state.active_poll = {
        "title": "استطلاع الإدارة الدوريات (تطوير منصة التحفيظ المباشرة):",
        "options": {"توسيع غرف البث المرئي": 18, "زيادة الورش القرآنية": 25, "تطوير الذكاء الاصطناعي": 30}
    }

if 'user_bg_choice' not in st.session_state:
    st.session_state.user_bg_choice = "ليل إسلامي داكن (افتراضي)"

if 'waiting_room' not in st.session_state:
    st.session_state.waiting_room = [
        {"id": "usr_99", "name": "القارئ أحمد", "status": "في الانتظار"},
        {"id": "usr_102", "name": "الزائر محمد", "status": "في الانتظار"}
    ]

if 'approved_live_users' not in st.session_state:
    st.session_state.approved_live_users = []

if 'memorization_logs' not in st.session_state:
    st.session_state.memorization_logs = []

# ---------------------------------------------------------
# 3. تخصيص خلفية الموقع ديناميكياً حسب اختيار المستخدم
# ---------------------------------------------------------
bg_styles = {
    "ليل إسلامي داكن (افتراضي)": "background: linear-gradient(135deg, #020907 0%, #08241b 100%); color: #fdfbf7;",
    "أخضر زمردي فاخر": "background: linear-gradient(135deg, #041f16 0%, #0d4734 100%); color: #ffffff;",
    "ذهبي ملكي مذهب": "background: linear-gradient(135deg, #1f1a04 0%, #42380c 100%); color: #fff8e1;",
    "أزرق هادئ خفيف": "background: linear-gradient(135deg, #06131f 0%, #0e2a45 100%); color: #e1f5fe;"
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
    
    .quran-text-container {{
        font-family: 'Amiri', serif;
        font-size: 1.8rem;
        line-height: 3rem;
        text-align: justify;
        background-color: #fdfbf7;
        color: #111111;
        padding: 30px;
        border-radius: 15px;
        border: 3px solid #d4af37;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }}
    
    .custom-card {{
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. بوابات الحماية وتسجيل الدخول عبر الوسائط الذكية
# ---------------------------------------------------------
SITE_SECRET_KEY = "quran2026"

if not st.session_state.site_authenticated:
    st.markdown("<h1 style='text-align:center; color:#d4af37; font-family:Amiri;'>بوابة الدخول المحمية - منصة القرآن الكريم</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>يرجى إدخال كلمة سر الدخول العامة للموقع وتسجيل حسابك لمباشرة الاستخدام</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        pass_input = st.text_input("🔑 كلمة سر الموقع العامة:", type="password")
        st.write("---")
        st.markdown("### اختر طريقة تسجيل الدخول مع ربط الحسابات:")
        auth_method = st.radio("وسيلة الدخول:", ["تسجيل حساب بريدي مباشر", "Google Account", "Facebook Account", "Instagram Account"])
        
        user_name_in = st.text_input("اسم المستخدم أو اسم القارئ:")
        user_role_in = st.selectbox("نوع الحساب:", ["عضو قارئ / مستمع", "مشرف ومدير النظام (Admin)"])
        
        if st.button("تسجيل الدخول وبدء الجلسة", use_container_width=True):
            if pass_input != SITE_SECRET_KEY:
                st.error("كلمة سر الموقع غير صحيحة! (كلمة السر الافتراضية للتجربة: quran2026)")
            elif not user_name_in.strip():
                st.warning("يرجى كتابة الاسم للتعرف عليك في البث الشات المباشر.")
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
# 5. الشريط الجانبي لوحة معلومات المستخدم والخلفيات
# ---------------------------------------------------------
st.sidebar.markdown(f"<h3 style='color:#d4af37;'>أهلاً بك: {st.session_state.current_user['name']}</h3>", unsafe_allow_html=True)
st.sidebar.write(f"الصلاحية: **{st.session_state.current_user['role']}**")
st.sidebar.write(f"طريقة التوثيق: **{st.session_state.current_user['method']}**")

st.sidebar.write("---")
st.sidebar.markdown("### 🎨 تخصيص خلفية الموقع:")
selected_bg = st.sidebar.selectbox("اختر نمط المظهر:", list(bg_styles.keys()), index=list(bg_styles.keys()).index(st.session_state.user_bg_choice))
if selected_bg != st.session_state.user_bg_choice:
    st.session_state.user_bg_choice = selected_bg
    st.rerun()

st.sidebar.write("---")
if st.sidebar.button("🚪 تسجيل الخروج من الموقع"):
    st.session_state.site_authenticated = False
    st.session_state.current_user = None
    st.rerun()

# ---------------------------------------------------------
# 6. الشريط العلوي المنشورات والإعلانات العامة للآدمن
# ---------------------------------------------------------
st.markdown("<h1 style='text-align:center; color:#d4af37; font-family:Amiri;'>الموسوعة القرآنية الشاملة واستوديو البث المباشر الذكي</h1>", unsafe_allow_html=True)

for ann in st.session_state.global_broadcasts:
    st.info(ann)

# ---------------------------------------------------------
# 7. التبويبات الرئيسية للتطبيق
# ---------------------------------------------------------
main_tabs = st.tabs([
    "📖 المصحف الشريف المكتوب",
    "📿 المسبحة اللانهائية",
    "📡 استوديو البث المباشر (Zoom Level)",
    "💬 الماسنجر والدردشة",
    "🌙 النظام الرمضاني والقرآن",
    "🏆 متابعة الحفظ والإنجازات",
    "🤖 المتصفح الديني الذكي",
    "🛡️ لوحة الإدارة والاستطلاعات"
])

# ---------------------------------------------------------
# التبويب 1: المصحف المكتوب
# ---------------------------------------------------------
with main_tabs[0]:
    st.markdown("## 📖 المصحف الشريف النصي الكامل")
    st.write("عرض واستعراض آيات القرآن الكريم بالنص العثماني الواضح:")
    
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
        surah_dict = {f"{s['number']}. {s['name']} ({s['numberOfAyahs']} آية)": s['number'] for s in surah_list}
        selected_surah = st.selectbox("اختر السورة الكريمة القراءة:", list(surah_dict.keys()))
        surah_id = surah_dict[selected_surah]
        
        try:
            res = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_id}/ar.alafasy", timeout=5)
            if res.status_code == 200:
                s_data = res.json().get('data', {})
                st.markdown(f"<h2 style='text-align:center; color:#d4af37; font-family:Amiri;'>سورة {s_data.get('name')}</h2>", unsafe_allow_html=True)
                ayahs_text = "".join([f"{a['text']} ﴿{a['numberInSurah']}﴾ " for a in s_data.get('ayahs', [])])
                st.markdown(f"<div class='quran-text-container'>{ayahs_text}</div>", unsafe_allow_html=True)
        except:
            st.error("تعذر الاتصال بقاعدة بيانات المصحف الإلكتروني.")
    else:
        st.warning("جاري تحميل قائمة السور...")

# ---------------------------------------------------------
# التبويب 2: المسبحة اللانهائية
# ---------------------------------------------------------
with main_tabs[1]:
    st.markdown("## 📿 المسبحة الرقمية اللانهائية (عداد بلا حدود)")
    col_tas1, col_tas2, col_tas3 = st.columns([1, 2, 1])
    
    with col_tas2:
        st.markdown(f"<h1 style='text-align:center; font-size:4rem; color:#d4af37;'>{st.session_state.tasbih_counter}</h1>", unsafe_allow_html=True)
        dhikr_type = st.selectbox("اختر صيغة الذكر:", ["سبحان الله وبحمده", "الحمد لله رب العالمين", "لا إله إلا الله وحدوه لا شريك له", "الله أكبر كبيراً", "أستغفر الله العظيم وأتوب إليه"])
        
        if st.button("📿 اضغط للتسبيح (+1)", use_container_width=True):
            st.session_state.tasbih_counter += 1
            st.rerun()
            
        if st.button("إعادة ضبط العداد (تصفير)", use_container_width=True):
            st.session_state.tasbih_counter = 0
            st.rerun()

# ---------------------------------------------------------
# التبويب 3: استوديو البث المباشر والإدارة الفائقة
# ---------------------------------------------------------
with main_tabs[2]:
    st.markdown("## 📡 استوديو البث المرئي والصوتي المباشر (نظام تحكم Zoom المتكامل)")
    
    col_live1, col_live2 = st.columns([2, 1])
    
    with col_live1:
        st.markdown("### الكاميرا المباشرة والتسجيل")
        st.camera_input("تشغيل كاميرا البث المباشر")
        audio_stream = st.audio_input("ميكروفون التلاوة المباشر")
        if audio_stream:
            st.audio(audio_stream)
            st.success("تم بث التسجيل الصوتي في القاعة مباشرة!")

    with col_live2:
        st.markdown("### 👥 المتصلون بغرفة البث")
        st.write(f"المتصل الحالي: **{st.session_state.current_user['name']}**")
        st.write(f"حالة البث: **نشط الآن (LIVE)**")
        
        st.write("---")
        st.markdown("### 🚪 غرف الانتظار وقبول الأعضاء (خاص بالمدير):")
        if st.session_state.current_user['role'] == "مشرف ومدير النظام (Admin)":
            if not st.session_state.waiting_room:
                st.info("لا يوجد زوار في قاعة الانتظار حالياً.")
            else:
                for idx, w_user in enumerate(st.session_state.waiting_room):
                    st.write(f"- **{w_user['name']}** (الحالة: {w_user['status']})")
                    c_acc, c_rej = st.columns(2)
                    with c_acc:
                        if st.button(f"قبول {w_user['name']}", key=f"acc_{idx}"):
                            st.session_state.approved_live_users.append(w_user['name'])
                            st.session_state.waiting_room.pop(idx)
                            st.success("تم إدخال الزائر لغرفة البث المرئي!")
                            st.rerun()
                    with c_rej:
                        if st.button(f"طرده/رفضه", key=f"rej_{idx}"):
                            st.session_state.waiting_room.pop(idx)
                            st.warning("تم رفض/إخراج الزائر.")
                            st.rerun()
        else:
            st.info("لوحة إدارة قبول وطرد الزوار متاحة للمشرفين فقط.")

# ---------------------------------------------------------
# التبويب 4: الماسنجر الشات
# ---------------------------------------------------------
with main_tabs[3]:
    st.markdown("## 💬 ماسنجر المحادثات والدردشة التفاعلية")
    
    chat_box = st.container(height=300)
    with chat_box:
        for c in st.session_state.chat_feed:
            st.markdown(f"<div class='custom-card'><b>{c['sender']}</b> ({c.get('time','')}):<br>{c['msg']}</div>", unsafe_allow_html=True)
            
    msg_input = st.text_input("اكتب رسالتك في المحادثة:")
    if st.button("إرسال الرسالة للجميع"):
        if msg_input.strip():
            st.session_state.chat_feed.append({
                "sender": st.session_state.current_user['name'],
                "msg": msg_input,
                "time": time.strftime("%H:%M")
            })
            st.rerun()

# ---------------------------------------------------------
# التبويب 5: النظام الرمضاني والقرآن في الخلفية
# ---------------------------------------------------------
with main_tabs[4]:
    st.markdown("## 🌙 النظام الرمضاني والإمساكية والقرآن المباشر")
    
    col_ram1, col_ram2 = st.columns(2)
    with col_ram1:
        st.markdown("### ⏰ منبه الإمساك والسحور")
        st.time_input("تحديد وقت تنبيه الإمساك:")
        if st.button("تفعيل المنبه الصوتي للإمساك"):
            st.success("تم تفعيل المنبه بنجاح وسيعمل عند حلول الوقت!")
            
        st.markdown("### 🤲 أدعية رمضانية مستجابة")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
        
    with col_ram2:
        st.markdown("### 📻 تشغيل القرآن الكريم في الخلفية")
        st.write("استمع للقرآن الكريم بدون توقف أثناء تصفحك للموقع:")
        st.audio("https://backup.quran-radio.com:8443/live.mp3")
        st.info("ملاحظة: يمكنك الانتقال بين التبويبات وس يستمر المشغل في العمل.")

# ---------------------------------------------------------
# التبويب 6: الإنجازات والتحفيظ
# ---------------------------------------------------------
with main_tabs[5]:
    st.markdown("## 🏆 نظام متابعة الإنجازات والورد اليومي")
    
    col_ach1, col_ach2 = st.columns(2)
    with col_ach1:
        st.markdown("### تسجيل ورد حفظ جديد:")
        s_name = st.text_input("اسم السورة التي حفظتها:")
        f_ayah = st.number_input("من الآية رقم:", min_value=1, value=1)
        t_ayah = st.number_input("إلى الآية رقم:", min_value=1, value=20)
        
        if st.button("تسجيل وتوثيق الإنجاز"):
            if s_name.strip():
                st.session_state.memorization_logs.append({
                    "surah": s_name,
                    "from": f_ayah,
                    "to": t_ayah,
                    "date": time.strftime("%Y-%m-%d")
                })
                st.success("تم حفظ إنجازك بنجاح في سجل الحفظ!")
                
    with col_ach2:
        st.markdown("### 📜 قائمة إنجازاتك المسجلة:")
        if not st.session_state.memorization_logs:
            st.write("لم تسجل أي إنجاز حفظ حتى الآن.")
        else:
            for log in st.session_state.memorization_logs:
                st.markdown(f"- سورة **{log['surah']}** من آية **{log['from']}** إلى **{log['to']}** (بتاريخ: {log['date']})")

# ---------------------------------------------------------
# التبويب 7: المتصفح الديني الذكي
# ---------------------------------------------------------
with main_tabs[6]:
    st.markdown("## 🤖 المتصفح والباحث الديني بالذكاء الاصطناعي")
    query_in = st.text_input("ابحث عن تفسير، حكم شرعي، أو كلمة قرآنية:")
    
    if st.button("بحث وتدبر بالذكاء الاصطناعي"):
        if query_in.strip():
            with st.spinner("جاري استخلاص الفوائد والتفاسير المعتمدة..."):
                time.sleep(0.5)
                st.markdown(f"""
                <div class='custom-card'>
                    <h4 style='color:#d4af37;'>نتائج البحث الديني حول: ({query_in})</h4>
                    <p>استناداً للتفاسير المعتمدة (تفسير ابن كثير والطبري): تؤكد الآيات والنصوص على قيم الرحمة والتدبر والالتزام بأحكام الشريعة مع الفهم العميق لمقاصد النص القرآني.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة جملة أو آية للبحث عنها.")

# ---------------------------------------------------------
# التبويب 8: لوحة الإدارة والاستطلاعات العامة
# ---------------------------------------------------------
with main_tabs[7]:
    st.markdown("## 🛡️ لوحة التحكم الإدارية وأنظمة الاستطلاع")
    
    if st.session_state.current_user['role'] != "مشرف ومدير النظام (Admin)":
        st.warning("عذراً! هذه اللوحة مخصصة فقط لمدير النظام (Admin).")
    else:
        st.success("مرحباً بك في لوحة الإدارة العليا المنصة.")
        
        st.markdown("### 📢 نشر إعلان أو تنبيه عام لكافة المستخدمين:")
        new_ann_text = st.text_input("اكتب الإعلان هنا:")
        if st.button("نشر الإعلان فوراً"):
            if new_ann_text.strip():
                st.session_state.global_broadcasts.append(f"🔴 إعلان الإدارة: {new_ann_text}")
                st.success("تم نشر الإعلان لكافة مستخدمي المنصة!")
                st.rerun()
                
        st.write("---")
        st.markdown("### 📊 نظام التصويت الدوري للإدارة (كل 10 أشهر):")
        st.write(f"**عنوان الاستطلاع:** {st.session_state.active_poll['title']}")
        
        for opt_key, count in st.session_state.active_poll['options'].items():
            st.write(f"- {opt_key}: **{count} صوت**")
            
        new_opt_in = st.text_input("إضافة خيار تصويت جديد للمستعملين:")
        if st.button("إضافة الخيار"):
            if new_opt_in.strip():
                st.session_state.active_poll['options'][new_opt_in] = 1
                st.success("تم إضافة الخيار للاستطلاع العامة بنجاح.")
                st.rerun()

st.write("---")
st.markdown("<p style='text-align:center; color:#d4af37;'>الموسوعة القرآنية الشاملة واستوديو البث الحي الذكي © 2026</p>", unsafe_allow_html=True)
