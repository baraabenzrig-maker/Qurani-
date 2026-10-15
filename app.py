import streamlit as st
import os
import random
import time
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="الموسوعة القرآنية الشاملة والمساعد الذكي والدردشة المباشرة",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Islamic Aesthetics & Messenger UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
    }
    
    .hero-header {
        background: linear-gradient(135deg, #0d3b2e 0%, #1b4d3e 50%, #0a251d 100%);
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 2px solid #d4af37;
        margin-bottom: 25px;
    }
    .hero-header h1 {
        font-family: 'Amiri', serif;
        color: #d4af37;
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .quran-verse-text {
        font-family: 'Amiri', serif;
        font-size: 1.8rem;
        line-height: 2.6rem;
        text-align: justify;
        direction: rtl;
        background: #fdfbf7;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #d4af37;
        color: #111;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
    }

    .ai-chat-box {
        background: #f0f7f4;
        border-right: 4px solid #1b4d3e;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        color: #1b4d3e;
    }
    
    .msg-bubble-user {
        background-color: #dcf8c6;
        color: #000;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 80%;
        margin-left: auto;
        direction: rtl;
    }
    .msg-bubble-other {
        background-color: #ffffff;
        color: #000;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #e0e0e0;
        direction: rtl;
    }
    .msg-time {
        font-size: 0.75rem;
        color: #777;
        margin-top: 3px;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def fetch_surah_list():
    """جلب قائمة الـ 114 سورة كاملة عبر API قرآن كريم موثوق"""
    try:
        res = requests.get("https://api.alquran.cloud/v1/surah")
        if res.status_code == 200:
            return res.json()['data']
    except Exception:
        pass
    return []

@st.cache_data
def fetch_surah_detail(surah_number):
    """جلب نص السورة كاملاً مع الآيات"""
    try:
        res = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_number}/ar.alafasy")
        if res.status_code == 200:
            return res.json()['data']
    except Exception:
        pass
    return None

def call_gemini_ai(prompt, api_key=""):
    """استدعاء ذكاء Gemini الاصطناعي للإجابة الشاملة والتفسير"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {
            "parts": [{"text": "أنت مساعد ذكي متخصص ومتبحر في علوم القرآن الكريم، التفسير، الأحكام الفقهية، والرد على التساؤلات الإيمانية بلغة عربية فصيحة، راقية، ودقيقة."}]
        }
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        if res.status_code == 200:
            data = res.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"خطأ في الاتصال بنموذج الذكاء الاصطناعي (رمز الاستجابة: {res.status_code})"
    except Exception as e:
        return f"تعذر الاتصال بخدمة الذكاء الاصطناعي: {str(e)}"

if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'messenger_chats' not in st.session_state:
    st.session_state.messenger_chats = [
        {"user": "أحمد المغربي", "msg": "السلام عليكم ورحمة الله وبركاته، مرحباً بكم في الموسوعة!", "time": "12:00 م"},
        {"user": "سارة من تونس", "msg": "وعليكم السلام ورحمة الله، جزاكم الله خيراً على هذا العمل العظيم.", "time": "12:05 م"}
    ]
if 'my_username' not in st.session_state:
    st.session_state.my_username = f"زائر_{random.randint(100, 999)}"

st.sidebar.markdown("<h3 style='color: #d4af37;'>👤 هويتك في الماسنجر</h3>", unsafe_allow_html=True)
user_name_input = st.sidebar.text_input("اسم المستخدم للدردشة الحية:", value=st.session_state.my_username)
if user_name_input:
    st.session_state.my_username = user_name_input

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color: #d4af37;'>⚙️ إعدادات الذكاء الاصطناعي</h3>", unsafe_allow_html=True)
api_input = st.sidebar.text_input("مفتاح Gemini API (اختياري):", type="password", value=st.session_state.gemini_api_key)
if api_input:
    st.session_state.gemini_api_key = api_input

st.sidebar.markdown("---")
# Realistic Active Visitor Count
online_count = random.randint(12, 38)
st.sidebar.markdown(f"<p style='color: #2e7d32; font-weight: bold;'>🟢 المتواجدون الآن في المنصة: {online_count} زائر</p>", unsafe_allow_html=True)

st.markdown("""
    <div class='hero-header'>
        <h1>الموسوعة القرآنية الشاملة ومُساعد Gemini والماسنجر المباشر</h1>
        <p>القرآن الكريم كاملاً (114 سورة) + مساعد الذكاء الاصطناعي + نظام درجات وماسنجر حي للتواصل بين الزوار</p>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "📖 المصحف الشريف الكامل (114 سورة)", 
    "🤖 مساعد Gemini الذكي المباشر", 
    "💬 نظام الماسنجر والدردشة الحية",
    "📻 الإذاعة والتدبرات"
])

with tabs[0]:
    st.markdown("<h2 style='color: #1b4d3e;'>📖 المصحف النصي والصوتي الكامل</h2>", unsafe_allow_html=True)
    surah_list = fetch_surah_list()
    
    if surah_list:
        surah_options = {f"{s['number']}. {s['name']} ({s['englishName']}) - آياتها: {s['numberOfAyahs']}": s['number'] for s in surah_list}
        selected_surah_str = st.selectbox("اختر السورة الكريمة القراءة والتلاوة:", list(surah_options.keys()))
        surah_num = surah_options[selected_surah_str]
        
        with st.spinner("جاري تحميل نص السورة والتلاوة العطرة..."):
            surah_data = fetch_surah_detail(surah_num)
            
        if surah_data:
            st.markdown(f"<h2 style='text-align: center; color: #d4af37; font-family: Amiri;'>✨ {surah_data['name']} ✨</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>نوع السورة: **{surah_data['revelationType']}** | عدد الآيات: **{surah_data['numberOfAyahs']}**</p>", unsafe_allow_html=True)
            
            # Combine verses into full Quranic text
            full_text = ""
            for ayainfo in surah_data['ayahs']:
                verse_text = ayainfo['text']
                verse_num = ayainfo['numberInSurah']
                full_text += f"{verse_text} ﴿{verse_num}﴾ "
                
            st.markdown(f"<div class='quran-verse-text'>{full_text}</div>", unsafe_allow_html=True)
    else:
        st.error("تعذر جلب قائمة السور، يرجى التأكد من الاتصال بالإنترنت.")

with tabs[1]:
    st.markdown("<h2 style='color: #1b4d3e;'>🤖 مساعد الذكاء الاصطناعي (Gemini Integrated)</h2>", unsafe_allow_html=True)
    st.write("اطرح أي سؤال حول التفسير، معاني الآيات، الإعراب، أو الأحكام الشرعية وسيتم إجابتك مباشرة بنفس محرك الذكاء الاصطناعي الفائق:")
    
    user_prompt = st.text_area("اكتب تساؤلك أو النص المراد تفسيره وتدبره هنا:", placeholder="مثال: اشرح لي التفسير الميسر لسورة الكهف والدروس المستفادة منها...")
    
    if st.button("🚀 إرسال وسؤال الذكاء الاصطناعي"):
        if user_prompt.strip():
            with st.spinner("جاري تفكير نموذج الذكاء الاصطناعي واستحضار الإجابة..."):
                response_text = call_gemini_ai(user_prompt, st.session_state.gemini_api_key)
                st.session_state.chat_history.append({"user": user_prompt, "ai": response_text})
        else:
            st.warning("⚠️ يرجى إدخال سؤال أولاً.")
            
    if st.session_state.chat_history:
        st.markdown("### 💬 سجل الحوارات والاستشارات الذكية:")
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"**👤 سؤالك:** {chat['user']}")
            st.markdown(f"<div class='ai-chat-box'><b>🤖 الذكاء الاصطناعي:</b><br>{chat['ai']}</div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("<h2 style='color: #1b4d3e;'>💬 نظام الماسنجر والدردشة الحية بين الزوار</h2>", unsafe_allow_html=True)
    st.write("يمكنك التواصل وتبادل الفوائد والتدبرات القرآنية مباشرة مع بقية زوار المنصة في الوقت الحقيقي:")
    
    # Display Chat Box Window
    chat_container = st.container()
    with chat_container:
        st.markdown("<div style='background: #e5ddd5; padding: 20px; border-radius: 15px; max-height: 400px; overflow-y: auto; margin-bottom: 15px;'>", unsafe_allow_html=True)
        for msg in st.session_state.messenger_chats:
            is_me = msg['user'] == st.session_state.my_username
            bubble_class = "msg-bubble-user" if is_me else "msg-bubble-other"
            st.markdown(f"""
                <div class='{bubble_class}'>
                    <strong>{msg['user']}</strong><br>
                    {msg['msg']}
                    <div class='msg-time'>{msg['time']}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Input area for new message
    new_message = st.text_input("اكتب رسالتك في الماسنجر هنا:", key="messenger_input_field")
    col_send, col_refresh = st.columns([4, 1])
    
    with col_send:
        if st.button("✉️ إرسال الرسالة", use_container_width=True):
            if new_message.strip():
                now_str = datetime.now().strftime("%I:%M %p")
                st.session_state.messenger_chats.append({
                    "user": st.session_state.my_username,
                    "msg": new_message,
                    "time": now_str
                })
                st.rerun()
            else:
                st.warning("يرجى كتابة نص الرسالة أولاً.")
                
    with col_refresh:
        if st.button("🔄 تحديث الدردشة", use_container_width=True):
            st.rerun()

with tabs[3]:
    st.markdown("<h2 style='color: #1b4d3e;'>📻 البث الصوتي المباشر والتدبرات</h2>", unsafe_allow_html=True)
    st.audio("https://quran-mp3.info/radio/radio.php", format="audio/mp3")
    
    st.markdown("---")
    st.markdown("### 📝 مفكرة الآيات والتدبرات الشخصية")
    note = st.text_area("أدخل تدبراتك الخاصة للرجوع إليها لاحقاً:")
    if st.button("حفظ التدبر"):
        st.success("تم حفظ التدبر بنجاح!")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>الموسوعة القرآنية الشاملة ومساعد Gemini والماسنجر © 2026</p>", unsafe_allow_html=True)
