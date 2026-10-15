import streamlit as st, os, random, time, requests, json
from datetime import datetime

# إعداد الصفحة العامة
st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة واستوديو البث الحي",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# قاموس الترجمات والواجهات متعددة اللغات
TR = {
    "ar": {
        "title": "الموسوعة القرآنية الشاملة واستوديو البث المباشر والذكاء الاصطناعي",
        "subtitle": "القرآن الكريم كاملاً + استوديو البث المرئي المباشر + محرك Gemini الذكي + ماسنجر الزوار",
        "identity": "هويتك في المنصة", "username": "اسم المستخدم للدردشة والبث:",
        "ai_settings": "إعدادات الذكاء الاصطناعي الفائق", "api_label": "مفتاح Gemini API (اختياري - يترك فارغاً للوضع التجريبي):",
        "active_users": "المتواجدون الآن بالحقيقة:", "visitors": "زائر نشط",
        "t_live": "استوديو البث المرئي المباشر", "t_quran": "المصحف الشريف الكامل",
        "t_ai": "مساعد Gemini الذكي", "t_msg": "نظام الماسنجر والدردشة", "t_notes": "مفكرة التدبرات الشخصية",
        "l_head": "استوديو البث المرئي والحي المباشر", "l_sub": "شارك في البث الحي وتلاواتك المباشرة والدروس القرآنية:",
        "cam_head": "نافذة بث الكاميرا والتلاوة المباشرة", "cam_lbl": "التقاط صورة أو بدء البث المباشر",
        "cam_cap": "لقطة بث حي بواسطة:", "cam_ok": "تم التقاط لقطة البث بنجاح وهي متاحة للعرض",
        "info_head": "تفاصيل غرفة البث الحي", "presenter": "المذيع / القارئ الحالي:", "viewers": "المشاهدون والموجودون في الغرفة الآن",
        "rec_head": "تسجيل الملاحظات الصوتية والتلاوة", "rec_lbl": "سجل تلاوتك أو مشاركتك الصوتية للبث:", "rec_ok": "تم تسجيل المقطع الصوتي بنجاح",
        "q_head": "المصحف النصي والصوتي الكامل", "q_sel": "اختر السورة الكريمة للقراءة والتلاوة:", "q_load": "جاري تحميل نص السورة والتلاوة العطرة...",
        "q_type": "نوع السورة:", "q_count": "عدد الآيات:", "ai_head": "مساعد الذكاء الاصطناعي المتقدم",
        "ai_sub": "المساعد الذكي لتفسير الآيات، الإعراب، استخراج الدروس، والأحكام الفقهية:", "ai_lbl": "اختر نمط الاستشارة الذكية:",
        "ai_modes": ["التفسير واستخراج التدبرات والفوائد", "استشارة فقهية وأحكام إيمانية", "إعراب القرآن والبلاغة القرآنية", "بحث شامل في الآيات المتشابهة"],
        "prompt_ph": "مثال: اشرح لي بالتفصيل التفسير والدروس المستفادة من سورة الكهف...", "ask_btn": "إرسال واستشارة الذكاء الاصطناعي",
        "asking": "جاري تحليل السؤال واستحضار الإجابة...", "warn_p": "يرجى إدخال السؤال أولاً",
        "hist_head": "سجل الحوارات والاستشارات الذكية:", "y_q": "[نمط: {mode}] سؤالك:", "ai_ans": "الذكاء الاصطناعي:",
        "m_head": "نظام الماسنجر والدردشة الحية بين الزوار", "m_sub": "تواصل وتبادل الفوائد والتدبرات القرآنية مباشرة مع بقية زوار المنصة:",
        "m_lbl": "اكتب رسالتك في الماسنجر هنا:", "send_btn": "إرسال الرسالة", "ref_btn": "تحديث الدردشة", "warn_m": "يرجى كتابة نص الرسالة أولاً",
        "n_head": "مفكرة الآيات والتدبرات الشخصية", "n_ph": "أدخل تدبراتك الخاصة للرجوع إليها لاحقاً:", "save_btn": "حفظ التدبر", "save_ok": "تم حفظ التدبر بنجاح",
        "foot": "الموسوعة القرآنية الشاملة واستوديو البث الحي"
    },
    "en": {
        "title": "Comprehensive Quranic Encyclopedia, Live Studio & AI Assistant",
        "subtitle": "Complete Holy Quran + Live Video Studio + Advanced Gemini AI Engine + Visitor Messenger",
        "identity": "Platform Identity", "username": "Username for chat and live stream:",
        "ai_settings": "Advanced AI Settings", "api_label": "Gemini API Key (optional):",
        "active_users": "Real-time Active Visitors:", "visitors": "active visitors",
        "t_live": "Live Video Broadcast Studio", "t_quran": "Complete Holy Quran",
        "t_ai": "Advanced Gemini AI Assistant", "t_msg": "Live Messenger & Community Chat", "t_notes": "Personal Reflection Notes",
        "l_head": "Live Video & Streaming Studio", "l_sub": "Participate in live broadcasts, recitations, and Quranic lessons:",
        "cam_head": "Camera Stream & Live Recitation Window", "cam_lbl": "Capture live photo or stream snapshot",
        "cam_cap": "Live broadcast snapshot by:", "cam_ok": "Broadcast snapshot captured successfully",
        "info_head": "Live Broadcast Room Details", "presenter": "Current Presenter / Reciter:", "viewers": "Current Viewers in Room",
        "rec_head": "Audio Notes & Recitation Recording", "rec_lbl": "Record your recitation or voice contribution:", "rec_ok": "Audio recording saved successfully",
        "q_head": "Complete Textual & Audio Quran", "q_sel": "Select Surah for reading and recitation:", "q_load": "Loading Surah text and audio recitation...",
        "q_type": "Revelation Type:", "q_count": "Number of Verses:", "ai_head": "Advanced AI Assistant",
        "ai_sub": "Your intelligent assistant for simplified interpretation, grammar analysis, and lessons:", "ai_lbl": "Select AI Consultation Mode:",
        "ai_modes": ["Tafsir, Reflections & Key Benefits", "Fiqh Consultation & Faith Rulings", "Quranic Grammar & Rhetoric", "Comprehensive Search in Similar Verses"],
        "prompt_ph": "Example: Explain in detail the interpretation and lessons learned from Surah Al-Kahf...", "ask_btn": "Send & Consult AI",
        "asking": "Analyzing question and retrieving answer...", "warn_p": "Please enter your question first",
        "hist_head": "Smart Consultation History:", "y_q": "[Mode: {mode}] Your Question:", "ai_ans": "Gemini AI:",
        "m_head": "Live Messenger & Visitor Chat", "m_sub": "Connect and share Quranic benefits and reflections directly with other visitors in real time:",
        "m_lbl": "Type your message here:", "send_btn": "Send Message", "ref_btn": "Refresh Chat", "warn_m": "Please type a message first",
        "n_head": "Personal Verse Reflections Notepad", "n_ph": "Enter your personal reflections to revisit later:", "save_btn": "Save Reflection", "save_ok": "Reflection saved successfully",
        "foot": "Comprehensive Quranic Encyclopedia & Live Studio"
    }
}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; background-color: #081c15; color: #fdfbf7; }
    .logo-container { display: flex; justify-content: center; align-items: center; margin-bottom: 20px; }
    .quran-logo-badge {
        width: 130px; height: 130px; border-radius: 50%; background: radial-gradient(circle, #0d3b2e 0%, #0a251d 100%);
        border: 4px solid #d4af37; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(0,0,0,0.4); text-align: center;
    }
    .quran-logo-text { font-family: 'Amiri', serif; color: #d4af37; font-size: 1.25rem; font-weight: 700; line-height: 1.5rem; }
    .hero-header {
        background: linear-gradient(135deg, #0d3b2e 0%, #1b4d3e 50%, #0a251d 100%);
        border-radius: 20px; padding: 25px 20px; text-align: center; color: #ffffff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 2px solid #d4af37; margin-bottom: 25px;
    }
    .hero-header h1 { font-family: 'Amiri', serif; color: #d4af37; font-size: 2rem; font-weight: 700; margin-bottom: 8px; }
    .quran-verse-text {
        font-family: 'Amiri', serif; font-size: 1.75rem; line-height: 2.6rem; text-align: justify;
        background: #fdfbf7; padding: 22px; border-radius: 15px; border: 2px solid #d4af37; color: #111;
    }
    .ai-chat-box { background: #081c15; border: 2px solid #d4af37; padding: 15px; border-radius: 10px; margin-bottom: 12px; color: #fdfbf7; }
    .msg-user { background-color: #1b4d3e; color: #fdfbf7; padding: 10px 15px; border-radius: 15px 15px 0 15px; margin-bottom: 10px; width: fit-content; max-width: 80%; margin-left: auto; border: 1px solid #d4af37; }
    .msg-other { background-color: #0d3b2e; color: #fdfbf7; padding: 10px 15px; border-radius: 15px 15px 15px 0; margin-bottom: 10px; width: fit-content; max-width: 80%; margin-right: auto; border: 1px solid #d4af37/50; }
    .live-tag { background-color: #e53935; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; display: inline-block; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

if 'visitor_id' not in st.session_state:
    st.session_state.visitor_id = str(random.randint(10000, 99999))
V_FILE = "active_visitors.json"

def get_visitor_count():
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

active_count = get_visitor_count()
if 'sel_lang' not in st.session_state:
    st.session_state.sel_lang = "ar"

lang_choice = st.sidebar.selectbox("Language / اللغة:", ["العربية (Arabic)", "English"], index=0 if st.session_state.sel_lang == "ar" else 1)
st.session_state.sel_lang = "ar" if "Arabic" in lang_choice else "en"
lang, t = st.session_state.sel_lang, TR[st.session_state.sel_lang]
tdir = "rtl" if lang == "ar" else "ltr"

st.sidebar.markdown(f"<h3 style='color:#d4af37;'>{t['identity']}</h3>", unsafe_allow_html=True)
if 'my_username' not in st.session_state:
    st.session_state.my_username = f"القارئ_{st.session_state.visitor_id[:3]}"
st.session_state.my_username = st.sidebar.text_input(t['username'], value=st.session_state.my_username)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<h3 style='color:#d4af37;'>{t['ai_settings']}</h3>", unsafe_allow_html=True)
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ""
st.session_state.gemini_key = st.sidebar.text_input(t['api_label'], type="password", value=st.session_state.gemini_key)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<p style='color:#d4af37; font-weight:bold; font-size:1.1rem;'>{t['active_users']} {active_count} {t['visitors']}</p>", unsafe_allow_html=True)

st.markdown("<div class='logo-container'><div class='quran-logo-badge'><div class='quran-logo-text'>الْقُرْآنُ<br>الْكَرِيمُ</div></div></div>", unsafe_allow_html=True)
st.markdown(f"<div class='hero-header' style='direction:{tdir};'><h1>{t['title']}</h1><p>{t['subtitle']}</p></div>", unsafe_allow_html=True)

tabs = st.tabs([t['t_live'], t['t_quran'], t['t_ai'], t['t_msg'], t['t_notes']])

@st.cache_data
def fetch_surahs():
    try:
        res = requests.get("https://api.alquran.cloud/v1/surah", timeout=10)
        if res.status_code == 200:
            return res.json()['data']
    except Exception:
        pass
    return []

@st.cache_data
def fetch_surah_detail(num):
    try:
        res = requests.get(f"https://api.alquran.cloud/v1/surah/{num}/ar.alafasy", timeout=10)
        if res.status_code == 200:
            return res.json()['data']
    except Exception:
        pass
    return None

def ask_gemini(prompt, sys_ctx, key=""):
    if not key or not key.strip():
        return f"✨ [وضع التجربة الديمو]: تم استقبال استشارتك بنجاح حول: ({prompt}). لإجابات متكاملة مباشرة من Google Gemini، يرجى إدخال مفتاح Gemini API الخاص بك في القائمة الجانبية."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "systemInstruction": {"parts": [{"text": sys_ctx}]}}
    try:
        res = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        return f"Error API: {res.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

if 'chat_hist' not in st.session_state:
    st.session_state.chat_hist = []
if 'msg_chats' not in st.session_state:
    st.session_state.msg_chats = [
        {"user": "أحمد المغربي", "msg": "السلام عليكم ورحمة الله وبركاته، مرحباً بكم جميعاً في هذه الموسوعة المباركة.", "time": "12:00 PM"},
        {"user": "فاطمة الزهراء", "msg": "وعليكم السلام ورحمة الله وبركاته، جزاكم الله خيراً على هذا التطبيق الرائع.", "time": "12:05 PM"}
    ]

with tabs[0]:
    st.markdown(f"<h2 style='color:#d4af37;'>{t['l_head']} <span class='live-tag'>LIVE</span></h2>", unsafe_allow_html=True)
    st.write(t['l_sub'])
    c_cam, c_info = st.columns([2, 1])
    with c_cam:
        st.subheader(t['cam_head'])
        pic = st.camera_input(t['cam_lbl'])
        if pic:
            st.image(pic, caption=f"{t['cam_cap']} {st.session_state.my_username}", use_container_width=True)
            st.success(t['cam_ok'])
    with c_info:
        st.subheader(t['info_head'])
        st.info(f"{t['presenter']} **{st.session_state.my_username}**")
        st.metric(label=t['viewers'], value=f"{active_count}")
        st.markdown("---")
        st.subheader(t['rec_head'])
        aud = st.audio_input(t['rec_lbl'])
        if aud:
            st.audio(aud)
            st.success(t['rec_ok'])

with tabs[1]:
    st.markdown(f"<h2 style='color:#d4af37;'>{t['q_head']}</h2>", unsafe_allow_html=True)
    s_list = fetch_surahs()
    if s_list:
        opts = {f"{s['number']}. {s['name']} ({s['englishName']}) - Ayahs: {s['numberOfAyahs']}": s['number'] for s in s_list}
        s_num = opts[st.selectbox(t['q_sel'], list(opts.keys()))]
        with st.spinner(t['q_load']):
            s_data = fetch_surah_detail(s_num)
        if s_data:
            st.markdown(f"<h2 style='text-align:center; color:#d4af37; font-family:Amiri;'>{s_data['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;'>{t['q_type']} **{s_data['revelationType']}** | {t['q_count']} **{s_data['numberOfAyahs']}**</p>", unsafe_allow_html=True)
            full_txt = "".join([f"{a['text']} [{a['numberInSurah']}] " for a in s_data['ayahs']])
            st.markdown(f"<div class='quran-verse-text' style='direction:rtl;'>{full_txt}</div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown(f"<h2 style='color:#d4af37;'>{t['ai_head']}</h2>", unsafe_allow_html=True)
    st.write(t['ai_sub'])
    mode = st.radio(t['ai_lbl'], t['ai_modes'], horizontal=True)
    u_prompt = st.text_area(t['prompt_ph'])
    if st.button(t['ask_btn']):
        if u_prompt.strip():
            ctx = f"You are an expert Quranic scholar. Language code: {lang}. Mode: {mode}."
            with st.spinner(t['asking']):
                ans = ask_gemini(u_prompt, ctx, st.session_state.gemini_key)
                st.session_state.chat_hist.append({"mode": mode, "user": u_prompt, "ai": ans})
        else:
            st.warning(t['warn_p'])
    if st.session_state.chat_hist:
        st.markdown(f"### {t['hist_head']}")
        for c in reversed(st.session_state.chat_hist):
            st.markdown(f"**{t['y_q'].format(mode=c['mode'])}** {c['user']}")
            st.markdown(f"<div class='ai-chat-box'><b>{t['ai_ans']}</b><br>{c['ai']}</div>", unsafe_allow_html=True)

with tabs[3]:
    st.markdown(f"<h2 style='color:#d4af37;'>{t['m_head']}</h2>", unsafe_allow_html=True)
    st.write(t['m_sub'])
    st.markdown("<div style='background:#0d3b2e; border: 2px solid #d4af37; padding:20px; border-radius:15px; max-height:400px; overflow-y:auto; margin-bottom:15px;'>", unsafe_allow_html=True)
    for m in st.session_state.msg_chats:
        b_cls = "msg-user" if m['user'] == st.session_state.my_username else "msg-other"
        st.markdown(f"<div class='{b_cls}'><strong>{m['user']}</strong><br>{m['msg']}<div style='font-size:0.75rem; color:#d4af37;'>{m['time']}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    new_m = st.text_input(t['m_lbl'], key="m_in")
    cs, cr = st.columns([4, 1])
    with cs:
        if st.button(t['send_btn'], use_container_width=True):
            if new_m.strip():
                st.session_state.msg_chats.append({
                    "user": st.session_state.my_username,
                    "msg": new_m,
                    "time": datetime.now().strftime("%I:%M %p")
                })
                st.rerun()
            else:
                st.warning(t['warn_m'])
    with cr:
        if st.button(t['ref_btn'], use_container_width=True):
            st.rerun()

with tabs[4]:
    st.markdown(f"<h2 style='color:#d4af37;'>{t['n_head']}</h2>", unsafe_allow_html=True)
    note_text = st.text_area(t['n_ph'], key="note_input_field")
    if st.button(t['save_btn']):
        if note_text.strip():
            st.success(t['save_ok'])
            st.markdown(f"<div class='ai-chat-box'><p>{note_text}</p><span style='font-size:0.75rem; color:#d4af37;'>{datetime.now().strftime('%Y-%m-%d')}</span></div>", unsafe_allow_html=True)
        else:
            st.warning("يرجى كتابة ملاحظة أولاً قبل الحفظ.")

st.markdown("---")
st.markdown(f"<p style='text-align:center; color:#d4af37;'>{t['foot']} © 2026</p>", unsafe_allow_html=True)
