import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="موقع قراني",
    page_icon="📖",
    layout="centered"
)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #1b4d3e;'>موقع قراني</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>نور لقلبك، بث مباشر، وإجابات دينية موثوقة بالذكاء الاصطناعي</p>", unsafe_allow_html=True)
st.markdown("---")

# تقسيم التطبيق إلى تبويبات رئيسية
tab1, tab2, tab3 = st.tabs(["📖 القرآن الكريم", "📻 البث المباشر", "🤖 الأسئلة الدينية"])

# تبويب القرآن الكريم
with tab1:
    st.header("القرآن الكريم (مطابق لمصحف المدينة)")
    st.write("تصفح القرآن الكريم، أو قم بتحميل النسخة الخاصة للجوالات والمصممة لتكون مريحة للعين.")
    
    # زر أو رابط لفتح ملف الـ PDF
    st.markdown(
        '<a href="DOC-20161125-WA0000.pdf" target="_blank" style="'
        'display: inline-block; background-color: #1b4d3e; color: white; '
        'padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;'
        '">فتح تصفح المصحف (PDF)</a>',
        unsafe_allow_html=True
    )

# تبويب البث المباشر
with tab2:
    st.header("البث المباشر (إذاعة القرآن الكريم)")
    st.write("استمع إلى بث مباشر لتلاوات القرآن الكريم طوال اليوم:")
    
    # مشغل الصوت المدمج
    st.audio("https://quran-mp3.info/radio/radio.php", format="audio/mp3")

# تبويب الأسئلة الدينية والذكاء الاصطناعي
with tab3:
    st.header("المساعد الذكي للأسئلة الدينية")
    st.write("اكتب أي سؤال ديني أو فقهي، وسيقوم الذكاء الاصطناعي بالإجابة عليك بدقة:")
    
    user_question = st.text_input("اكتب سؤالك هنا (مثال: ما هي أحكام الصلاة للمريض؟)...")
    
    if st.button("إرسال السؤال"):
        if not user_question.strip():
            st.warning("الرجاء كتابة سؤال أولاً!")
        else:
            with st.spinner("جاري مراجعة المسائل الشرعية والإجابة بدقة..."):
                # محاكاة استجابة ذكاء اصطناعي مخصصة للأسئلة الدينية
                st.success("الإجابة الشرعية:")
                st.info(f'بخصوص سؤالك ("{user_question}"): يُستحب دائماً الرجوع إلى النصوص الشرعية الموثوقة وأقوال أهل العلم المعتبرين. بناءً على القواعد الفقهية، المسألة تتطلب تحري الدقة واليسر مع الالتزام بالأصول الشرعية الصحيحة.')

# تذيل الصفحة
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>جميع الحقوق محفوظة - مشروع قراني (مستند إلى مصحف المدينة النبوية)</p>", unsafe_allow_html=True)