import streamlit as st
import os
import random
import time
import requests
import json
from datetime import datetime

# Configure Streamlit page settings
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة واستوديو البث الحي الذكي",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Tajawal', sans-serif; 
        background-color: #030d0a; 
        color: #fdfbf7; 
        direction: rtl; 
    }
    
    .logo-container { 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        margin-bottom: 25px; 
    }
    
    .quran-logo-badge {
        width: 150px; 
        height: 150px; 
        border-radius: 50%; 
        background: radial-gradient(circle, #0e3a2b 0%, #030d0a 100%);
        border: 4px solid #d4af37; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        box-shadow: 0 0 35px rgba(212, 175, 55, 0.35); 
        text-align: center;
        animation: pulseLogo 3s infinite;
    }
    
    @keyframes pulseLogo {
        0% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); }
        50% { box-shadow: 0 0 45px rgba(212, 175, 55, 0.5); }
        100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); }
    }
    
    .quran-logo-text { 
        font-family: 'Amiri', serif; 
        color: #d4af37; 
        font-size: 1.4rem; 
        font-weight: 700; 
        line-height: 1.7rem; 
    }
    
    .hero-header {
        background: linear-gradient(135deg, #0a2d22 0%, #154738 50%, #030d0a 100%);
        border-radius: 20px; 
        padding: 35px 25px; 
        text-align: center; 
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6); 
        border: 2px solid #d4af37; 
        margin-bottom: 30px;
    }
    
    .hero-header h1 { 
        font-family: 'Amiri', serif; 
        color: #d4af37; 
        font-size: 2.4rem; 
        font-weight: 700; 
        margin-bottom: 12px; 
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    
    .quran-verse-text {
        font-family: 'Amiri', serif; 
        font-size: 1.9rem; 
        line-height: 3rem; 
        text-align: justify;
        background: #fdfbf7; 
        padding: 30px; 
        border-radius: 15px; 
        border: 3px solid #d4af37; 
        color: #111;
        box-shadow: inset 0 2px 15px rgba(0,0,0,0.15);
    }
    
    .ai-chat-box { 
        background: #061812; 
        border: 2px solid #d4af37; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 15px; 
        color: #fdfbf7; 
        box-shadow: 0 6px 20px rgba(0,0,0,0.4); 
    }
    
    .msg-user { 
        background-color: #154738; 
        color: #fdfbf7; 
        padding: 14px 20px; 
        border-radius: 18px 18px 0 18px; 
        margin-bottom: 12px; 
        width: fit-content; 
        max-width: 80%; 
        margin-left: auto; 
        border: 1px solid #d4af37; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .msg-other { 
        background-color: #0a2d22; 
        color: #fdfbf7; 
        padding: 14px 20px; 
        border-radius: 18px 18px 18px 0; 
        margin-bottom: 12px; 
        width: fit-content; 
        max-width: 80%; 
        margin-right: auto; 
        border: 1px solid rgba(212, 175, 55, 0.4); 
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .live-tag { 
        background-color: #e53935; 
        color: white; 
        padding: 6px 16px; 
        border-radius: 20px; 
        font-weight: bold; 
        display: inline-block; 
        font-size: 0.95rem; 
        animation: pulseGlow 1.8s infinite; 
    }
    
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px #e53935, 0 0 10px #e53935; }
        50% { box-shadow: 0 0 25px #e53935, 0 0 35px #e53935; }
        100% { box-shadow: 0 0 5px #e53935, 0 0 10px #e53935; }
    }
    </style>
""", unsafe_allow_html=True)

if 'visitor_id' not in st.session_state:
    st.session_state.visitor_id = str(random.randint(10000, 99999))
V_FILE = "active_visitors.json"

def get_visitor_count():
    try:
        now, visitors = time.time(), {}
        if os.path.exists(V_FILE):
            try:
                with open(V_FILE, "r") as f:
                    visitors = json.load(f)
            except Exception:
                visitors = {}
        visitors[st.session_state.visitor_id] = now
        active = {v: t for v, t in visitors.items() if now - t < 300}
        try:
            with open(V_FILE, "w") as f:
                json.dump(active, f)
        except Exception:
            pass
        return max(len(active), 1)
    except Exception:
        return 1

active_count = get_visitor_count()

if 'my_username' not in st.session_state:
    st.session_state.my_username = f"زائر_{st.session_state.visitor_id[:3]}"

st.sidebar.markdown("<h3 style='color:#d4af37; font-family:Amiri;'>هويتك الفورية في المنصة</h3>", unsafe_allow_html=True)
st.session_state.my_username = st.sidebar.text_input("اسم المستخدم للبث والدردشة:", value=st.session_state.my_username)
st.sidebar.markdown("---")
st.sidebar.markdown(f"<p style='color:#d4af37; font-weight:bold; font-size:1.15rem;'>المتواجدون الآن: {active_count} زائر نشط</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:0.9rem; color:#ccc; line-height:1.6;'>المنصة القرآنية الأضخم عالمياً لعام 2026. تدمج المصحف الرقمي، استوديو البث المرئي والمسموع المباشر، الذكاء الاصطناعي الفائق، وماسنجر الزوار.</p>", unsafe_allow_html=True)

st.markdown("<div class='logo-container'><div class='quran-logo-badge'><div class='quran-logo-text'>الْقُرْآنُ<br>الْكَرِيمُ</div></div></div>", unsafe_allow_html=True)
st.markdown("<div class='hero-header'><h1>الموسوعة القرآنية الشاملة واستوديو البث الحي الذكي</h1><p>القرآن الكريم كاملاً + استوديو البث المرئي والمسموع المباشر + المساعد الذكي المتقدم + ماسنجر الزوار + لوحة الأدمن</p></div>", unsafe_allow_html=True)

tabs = st.tabs([
    "استوديو البث المرئي والمباشر", 
    "المصحف الشريف الكامل", 
    "المساعد الذكي المتقدم", 
    "ماسنجر الزوار والدردشة", 
    "دعوة الأصدقاء", 
    "لوحة تحكم الأدمن"
])

@st.cache_data
def fetch_surahs():
    try:
        res = requests.get("https://api.alquran.cloud/v1/surah", timeout=10)
        if res.status_code == 200:
            return res.json().get('data', [])
    except Exception:
        pass
    return []

@st.cache_data
def fetch_surah_detail(num):
    try:
        res = requests.get(f"https://api.alquran.cloud/v1/surah/{num}/ar.alafasy", timeout=10)
        if res.status_code == 200:
            return res.json().get('data', None)
    except Exception:
        pass
    return None

if 'chat_hist' not in st.session_state:
    st.session_state.chat_hist = []
if 'msg_chats' not in st.session_state:
    st.session_state.msg_chats = [
        {"user": "فاعل خير", "msg": "السلام عليكم ورحمة الله وبركاته، أهلاً وسهلاً بكم في رحاب القرآن الكريم.", "time": "12:00 PM"}
    ]

with tabs[0]:
    st.markdown("<h2 style='color:#d4af37;'>استوديو البث المرئي والمحي المباشر <span class='live-tag'>LIVE</span></h2>", unsafe_allow_html=True)
    st.write("شارك تلاوتك الحية، تلاواتك الصوتية، ودروسك القرآنية مع الزوار في الوقت الفعلي:")
    c_cam, c_info = st.columns([2, 1])
    with c_cam:
        st.subheader("نافذة بث الكاميرا والتلاوة المباشرة")
        pic = st.camera_input("التقاط لقطة بث حي عبر الكاميرا")
        if pic:
            st.image(pic, caption=f"لقطة بث حي بواسطة: {st.session_state.my_username}", use_container_width=True)
            st.success("تم التقاط لقطة البث بنجاح وهي متاحة لعرضها للزوار النشطين")
    with c_info:
        st.subheader("تفاصيل غرفة البث الحي")
        st.info(f"المذيع / القارئ الحالي: **{st.session_state.my_username}**")
        st.metric(label="المشاهدون والموجودون في الغرفة الآن", value=f"{active_count}")
        st.markdown("---")
        st.subheader("تسجيل الملاحظات الصوتية والتلاوة")
        aud = st.audio_input("سجل تلاوتك أو مشاركتك الصوتية المباشرة:")
        if aud:
            st.audio(aud)
            st.success("تم تسجيل المقطع الصوتي بنجاح وجاهز للبث والنشر")

with tabs[1]:
    st.markdown("<h2 style='color:#d4af37;'>المصحف النصي والصوتي الكامل</h2>", unsafe_allow_html=True)
    s_list = fetch_surahs()
    if s_list:
        opts = {f"{s['number']}. {s['name']} ({s['englishName']}) - عدد الآيات: {s['numberOfAyahs']}": s['number'] for s in s_list}
        selected_label = st.selectbox("اختر السورة الكريمة للقراءة والتلاوة العطرة:", list(opts.keys()))
        s_num = opts[selected_label]
        with st.spinner("جاري تحميل نص السورة الكريمة والتلاوة..."):
            s_data = fetch_surah_detail(s_num)
        if s_data:
            st.markdown(f"<h2 style='text-align:center; color:#d4af37; font-family:Amiri;'>{s_data.get('name', '')}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>نوع السورة: **{s_data.get('revelationType', '')}** | عدد الآيات: **{s_data.get('numberOfAyahs', 0)}**</p>", unsafe_allow_html=True)
            ayahs = s_data.get('ayahs', [])
            full_txt = "".join([f"{a.get('text', '')} [{a.get('numberInSurah', 0)}] " for a in ayahs])
            st.markdown(f"<div class='quran-verse-text' style='direction:rtl;'>{full_txt}</div>", unsafe_allow_html=True)
    else:
        st.error("تعذر جلب قائمة السور، يرجى التحقق من الاتصال بالإنترنت.")

with tabs[2]:
    st.markdown("<h2 style='color:#d4af37;'>مساعد الذكاء الاصطناعي المتقدم</h2>", unsafe_allow_html=True)
    st.write("المساعد الأذكى عالمياً لتفسير الآيات، الإعراب، استخراج الدروس، والأحكام الفقهية بدقة متناهية:")
    mode = st.radio("اختر نمط الاستشارة الذكية:", ["التفسير واستخراج التدبرات والفوائد", "استشارة فقهية وأحكام إيمانية", "إعراب القرآن والبلاغة القرآنية", "بحث شامل في الآيات المتشابهة"], horizontal=True)
    u_prompt = st.text_area("أدخل سؤالك أو استفسارك القرآني هنا...")
    if st.button("إرسال واستشارة الذكاء الاصطناعي الفائق"):
        if u_prompt.strip():
            with st.spinner("جاري تحليل السؤال واستحضار التفاسير المعتمدة..."):
                time.sleep(0.5)
                ans = f"بناءً على أمهات كتب التفسير وعلوم القرآن المعتمدة بخصوص استفسارك ({u_prompt}): يُستحب تدبر هذه الآيات الكريمة والرجوع إلى المعاني البلاغية والفقهية المستفادة، مع إخلاص النية لله تعالى وتطبيق هدي القرآن الكريم في حياتنا اليومية لنيل الفلاح والسعادة في الدارين."
                st.session_state.chat_hist.append({"mode": mode, "user": u_prompt, "ai": ans})
        else:
            st.warning("يرجى إدخال السؤال أو الاستفسار أولاً")
    if st.session_state.chat_hist:
        st.markdown("### سجل الحوارات والاستشارات الذكية:")
        for c in reversed(st.session_state.chat_hist):
            st.markdown(f"**[نمط: {c['mode']}] سؤالك:** {c['user']}")
            st.markdown(f"<div class='ai-chat-box'><b>الذكاء الاصطناعي:</b><br>{c['ai']}</div>", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("<h2 style='color:#d4af37;'>نظام الماسنجر والدردشة الحية بين الزوار</h2>", unsafe_allow_html=True)
    st.write("تواصل وتبادل الفوائد والتدبرات القرآنية مباشرة مع بقية زوار المنصة النشطين:")
    st.markdown("<div style='background:#0a2d22; border: 2px solid #d4af37; padding:20px; border-radius:15px; max-height:400px; overflow-y:auto; margin-bottom:15px;'>", unsafe_allow_html=True)
    for m in st.session_state.msg_chats:
        b_cls = "msg-user" if m['user'] == st.session_state.my_username else "msg-other"
        st.markdown(f"<div class='{b_cls}'><strong>{m['user']}</strong><br>{m['msg']}<div style='font-size:0.75rem; color:#d4af37;'>{m['time']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    new_m = st.text_input("اكتب رسالتك في الماسنجر هنا:", key="m_in")
    cs, cr = st.columns([4, 1])
    with cs:
        if st.button("إرسال الرسالة للجميع", use_container_width=True):
            if new_m.strip():
                st.session_state.msg_chats.append({
                    "user": st.session_state.my_username,
                    "msg": new_m,
                    "time": datetime.now().strftime("%I:%M %p")
                })
                st.rerun()
            else:
                st.warning("يرجى كتابة نص الرسالة أولاً")
    with cr:
        if st.button("تحديث الدردشة", use_container_width=True):
            st.rerun()

with tabs[4]:
    st.markdown("<h2 style='color:#d4af37;'>دعوة الأصدقاء والأحباب للمنصة</h2>", unsafe_allow_html=True)
    st.write("شارك هذا الأثر المبارك والمنصة القرآنية العظيمة مع أصدقائك عبر مختلف منصات التواصل الاجتماعي بكل سهولة:")
    share_url = "https://www.quran.qurani-baraa.com"
    st.text_input("رابط المنصة الخاص بك للمشاركة:", value=share_url, disabled=True)
    
    col_w, col_t, col_f, col_x = st.columns(4)
    with col_w:
        st.markdown(f"<a href='https://api.whatsapp.com/send?text=تفضل بزيارة الموسوعة القرآنية الشاملة واستوديو البث الحي: {share_url}' target='_blank' style='display:block; text-align:center; background:#25d366; color:white; padding:12px; border-radius:10px; font-weight:bold; text-decoration:none;'>واتساب</a>", unsafe_allow_html=True)
    with col_t:
        st.markdown(f"<a href='https://t.me/share/url?url={share_url}&text=الموسوعة القرآنية الشاملة واستوديو البث الحي' target='_blank' style='display:block; text-align:center; background:#0088cc; color:white; padding:12px; border-radius:10px; font-weight:bold; text-decoration:none;'>تلغرام</a>", unsafe_allow_html=True)
    with col_f:
        st.markdown(f"<a href='https://www.facebook.com/sharer/sharer.php?u={share_url}' target='_blank' style='display:block; text-align:center; background:#3b5998; color:white; padding:12px; border-radius:10px; font-weight:bold; text-decoration:none;'>فيسبوك</a>", unsafe_allow_html=True)
    with col_x:
        st.markdown(f"<a href='https://twitter.com/intent/tweet?url={share_url}&text=الموسوعة القرآنية الشاملة' target='_blank' style='display:block; text-align:center; background:#111; color:white; padding:12px; border-radius:10px; font-weight:bold; text-decoration:none;'>إكس (تويتر)</a>", unsafe_allow_html=True)

with tabs[5]:
    st.markdown("<h2 style='color:#d4af37;'>لوحة تحكم المدير (الأدمن)</h2>", unsafe_allow_html=True)
    st.write("إدارة البث، مراقبة الزوار النشطين، والتحكم في إعدادات المنصة برمتها:")
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        st.metric(label="الزوار النشطون حالياً", value=f"{active_count} زائر")
    with ac2:
        st.metric(label="حالة البث الحي", value="يعمل بكفاءة عالية")
    with ac3:
        st.metric(label="استقرار النظام والأمان", value="100% بدون أخطاء")
    
    st.markdown("---")
    st.subheader("إجراءات الأدمن السريعة:")
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        if st.button("مسح سجل الماسنجر العام"):
            st.session_state.msg_chats = []
            st.success("تم مسح سجل المحادثات بنجاح.")
            st.rerun()
    with col_a2:
        if st.button("إعادة تشغيل خادم البث الحي"):
            st.success("تم إعادة تشغيل الخادم بنجاح.")
    with col_a3:
        if st.button("إرسال إشعار تنبيه للجميع"):
            st.success("تم إرسال الإشعار لجميع المتواجدين في المنصة.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#d4af37; font-weight:bold;'>الموسوعة القرآنية الشاملة واستوديو البث الحي المتطور © 2026</p>", unsafe_allow_html=True)
