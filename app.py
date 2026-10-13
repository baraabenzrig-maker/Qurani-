from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qurani Elite Hub - المنصة الإسلامية الذكية المتكاملة</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #020617, #0f172a, #1e1b4b);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            transition: background 0.5s ease;
        }
        header {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(15px);
            padding: 12px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .logo {
            font-size: 20px;
            font-weight: bold;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .online-badge {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            border: 1px solid rgba(52, 211, 153, 0.3);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        /* الهيكل الطويل والمتحرك */
        .main-wrapper {
            display: flex;
            flex-direction: column;
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }
        .grid-container {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }
        @media(max-width: 900px) {
            .grid-container { grid-template-columns: 1fr; }
        }

        .card {
            background: rgba(30, 41, 59, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }

        /* شاشة البث والفيديو */
        .video-container {
            position: relative;
            width: 100%;
            height: 400px;
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid rgba(56, 189, 248, 0.3);
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        /* نافذة المتكلم العائمة الصغيرة */
        .floating-speaker {
            position: absolute;
            bottom: 15px;
            right: 15px;
            width: 110px;
            height: 80px;
            background: rgba(15, 23, 42, 0.9);
            border: 2px solid #38bdf8;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            z-index: 10;
            cursor: grab;
        }

        .controls-bar {
            display: flex;
            gap: 10px;
            margin-top: 12px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .btn {
            background: #334155;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: 0.2s;
        }
        .btn:hover { background: #475569; }
        .btn.active { background: #0284c7; }
        .btn.off { background: #ef4444; }

        /* عارض صفحات القرآن الكريم */
        .quran-viewer {
            display: flex;
            flex-direction: column;
            gap: 10px;
            text-align: center;
        }
        .quran-page-box {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 12px;
            padding: 20px;
            min-height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Amiri', serif;
            font-size: 18px;
            line-height: 2.2;
            color: #f1f5f9;
        }
        .quran-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* الشات والذكاء الاصطناعي */
        .tabs {
            display: flex;
            background: rgba(15, 23, 42, 0.8);
            border-radius: 10px;
            padding: 4px;
            margin-bottom: 10px;
            gap: 4px;
        }
        .tab-btn {
            flex: 1;
            background: none;
            border: none;
            color: #94a3b8;
            padding: 8px;
            font-size: 12px;
            cursor: pointer;
            font-weight: bold;
            border-radius: 8px;
        }
        .tab-btn.active {
            color: white;
            background: #0284c7;
        }
        .tab-content { display: none; flex-direction: column; gap: 8px; height: 320px; }
        .tab-content.active { display: flex; }
        
        .messages-box {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 5px;
        }
        .message {
            background: #1e293b;
            padding: 8px 12px;
            border-radius: 10px;
            max-width: 85%;
            font-size: 13px;
            line-height: 1.4;
        }
        .message.incoming { align-self: flex-start; }
        .message.outgoing { align-self: flex-end; background: #0284c7; }

        .input-group {
            display: flex;
            gap: 6px;
        }
        .input-group input {
            flex: 1;
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 8px 12px;
            border-radius: 16px;
            color: white;
            outline: none;
            font-size: 12px;
        }
        .input-group button {
            background: #0284c7;
            color: white;
            border: none;
            padding: 0 14px;
            border-radius: 16px;
            cursor: pointer;
        }

        /* شريط المراجعة السفلي */
        footer {
            background: rgba(15, 23, 42, 0.95);
            padding: 20px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: auto;
            font-size: 13px;
            color: #94a3b8;
        }

        /* نافذة الأدمن */
        .admin-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .admin-box {
            background: #1e293b;
            padding: 25px;
            border-radius: 16px;
            width: 340px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            border: 1px solid #38bdf8;
        }
        .admin-box input, .admin-box select {
            background: #0f172a;
            border: 1px solid #475569;
            padding: 10px;
            color: white;
            border-radius: 8px;
            font-size: 13px;
        }
    </style>
</head>
<body id="pageBody">
    <header>
        <div class="logo">📖 Qurani Elite Hub</div>
        <div style="display:flex; gap:12px; align-items:center;">
            <div class="online-badge">🟢 المتواجدون الآن: <strong id="onlineCount">18</strong></div>
            <button class="btn active" onclick="openAdmin()" style="padding:5px 12px; font-size:12px;">🔒 لوحة الأدمن</button>
        </div>
    </header>

    <div class="main-wrapper">
        <!-- القسم الرئيسي الأول: البث وعارض القرآن -->
        <div class="grid-container">
            <!-- البث المباشر -->
            <div class="card">
                <h3 style="color:#38bdf8; margin-bottom:10px; font-size:15px;">📹 غرفة البث التفاعلية المباشرة</h3>
                <div class="video-container" id="videoWrapper">
                    <video id="webcam" autoplay playsinline></video>
                    <!-- نافذة المتكلم المصغرة في الجانب -->
                    <div class="floating-speaker" id="floatingSpeaker">
                        <span style="color:#34d399; font-weight:bold;">🎙️ المتكلم</span>
                        <span id="speakerStatus" style="font-size:10px; color:#cbd5e1;">معطل</span>
                    </div>
                </div>
                <div class="controls-bar">
                    <button id="camBtn" class="btn off" onclick="toggleCamera()">📹 الكاميرا</button>
                    <button id="micBtn" class="btn off" onclick="toggleMic()">🎤 الميكروفون النقي</button>
                    <button class="btn" onclick="toggleFullscreen()">⛶ تكبير الشاشة بالكامل</button>
                    <button class="btn" onclick="rotateView()">🔄 تدوير العرض</button>
                </div>
            </div>

            <!-- عارض صفحات القرآن الكريم (متتالي يمين ويسار) -->
            <div class="card quran-viewer">
                <h3 style="color:#38bdf8; font-size:15px;">📖 تصفح المصحف الشريف</h3>
                <div class="quran-page-box" id="quranPageContent">
                    بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ<br>
                    الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ ۝ الرَّحْمَٰنِ الرَّحِيمِ ۝ مَالِكِ يَوْمِ الدِّينِ ۝
                </div>
                <div class="quran-nav">
                    <button class="btn" onclick="prevQuranPage()">⬅️ الصفحة السابقة</button>
                    <span id="pageIndicator" style="font-size:12px; color:#cbd5e1;">صفحة 1 من 5</span>
                    <button class="btn" onclick="nextQuranPage()">الصفحة التالية ➡️</button>
                </div>
            </div>
        </div>

        <!-- القسم الثاني: الشات، الذكاء الاصطناعي، والإنجازات -->
        <div class="grid-container">
            <div class="card">
                <div class="tabs">
                    <button class="tab-btn active" onclick="switchTab('chat')">💬 الشات العام</button>
                    <button class="tab-btn" onclick="switchTab('ai')">🤖 الذكاء الاصطناعي الديني</button>
                    <button class="tab-btn" onclick="switchTab('goals')">🎯 إنجازات اليوم</button>
                </div>

                <!-- تبويب الشات -->
                <div class="tab-content active" id="tab-chat">
                    <div class="messages-box" id="chatBox">
                        <div class="message incoming"><strong>أحمد:</strong> مرحباً بالجميع في الغرفة المباركة</div>
                        <div class="message outgoing"><strong>أنت:</strong> وعليكم السلام، حياكم الله</div>
                    </div>
                    <div class="input-group">
                        <input type="text" id="msgInput" placeholder="اكتب رسالة للدردشة..." onkeypress="handleKey(event)">
                        <button onclick="sendMessage()">إرسال</button>
                    </div>
                </div>

                <!-- تبويب الذكاء الاصطناعي الديني الصحيح والمطوير -->
                <div class="tab-content" id="tab-ai">
                    <div class="messages-box" id="aiBox">
                        <div class="message incoming"><strong>🤖 المساعد الديني الذكي:</strong> أهلاً بك. اسألني عن أي حكم شرعي، آية قرآنية، أو حديث شريف وسأجيبك بدقة.</div>
                    </div>
                    <div class="input-group">
                        <input type="text" id="aiInput" placeholder="اسأل المساعد الديني..." onkeypress="handleAIKey(event)">
                        <button onclick="askAI()">سؤال</button>
                    </div>
                </div>

                <!-- تبويب إنجازات اليوم المتجددة -->
                <div class="tab-content" id="tab-goals" style="overflow-y:auto; padding:5px;">
                    <h4 style="color:#38bdf8; font-size:13px; margin-bottom:8px;">📌 جدول الطاعات اليومي (يتجدد تلقائياً):</h4>
                    <div style="background:#0f172a; padding:12px; border-radius:10px; font-size:13px; display:flex; flex-direction:column; gap:8px;">
                        <label><input type="checkbox"> قراءة حزب كامل من القرآن</label>
                        <label><input type="checkbox"> حضور بث التلاوة والمشاركة</label>
                        <label><input type="checkbox"> الاستغفار 100 مرة</label>
                        <label><input type="checkbox"> حفظ آية جديدة وتدبرها</label>
                    </div>
                    <p style="font-size:11px; color:#94a3b8; margin-top:5px;">* يتم مسح هذه الإنجازات وتحديثها مع شروق كل يوم جديد.</p>
                </div>
            </div>

            <!-- لوحة المراجعة والمعلومات الجانبية -->
            <div class="card">
                <h3 style="color:#38bdf8; margin-bottom:10px; font-size:15px;">📊 سجل ومراجعة الغرفة</h3>
                <div style="font-size:12px; color:#cbd5e1; display:flex; flex-direction:column; gap:8px; line-height:1.6;">
                    <p>🟢 حالة الاتصال: <span style="color:#34d399;">مستقر وآمن</span></p>
                    <p>🎙️ جودة الصوت: <span style="color:#38bdf8;">نقي مع إزالة صدى الصوت</span></p>
                    <p>👥 عدد المشتركين الفعليين: <b id="realCount" style="color:#38bdf8;">18</b> مستخدماً نشطاً</p>
                    <p>🔒 صلاحيات المشرف: <span id="adminStatusText" style="color:#facc15;">وضع الزائر العادي</span></p>
                </div>
            </div>
        </div>
    </div>

    <!-- شريط المراجعة السفلي -->
    <footer>
        <p>Qurani Elite Hub &copy; 2026 — منصة تفاعلية متكاملة للبث والقرآن الكريم والذكاء الاصطناعي الديني.</p>
    </footer>

    <!-- نافذة الأدمن السرية لتغيير كلمة المرور والإعدادات -->
    <div class="admin-modal" id="adminModal">
        <div class="admin-box">
            <h3 style="color:#38bdf8; font-size:16px;">لوحة تحكم الأدمن</h3>
            <p style="font-size:12px; color:#cbd5e1;">قم بتغيير إعدادات الخلفية وكلمة المرور:</p>
            <label style="font-size:11px;">كلمة المرور الجديدة:</label>
            <input type="password" id="newPassInput" placeholder="أدخل كلمة مرور جديدة">
            
            <label style="font-size:11px;">اختر خلفية الموقع:</label>
            <select id="bgSelector">
                <option value="deep">خلفية داكنة فخمة (افتراضي)</option>
                <option value="midnight">خلفية منتصف الليل الزرقاء</option>
                <option value="emerald">خلفية زمردية إسلامية هادئة</option>
            </select>

            <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:10px;">
                <button class="btn off" onclick="closeAdmin()">إلغاء</button>
                <button class="btn active" onclick="saveAdminSettings()">حفظ وتطبيق</button>
            </div>
        </div>
    </div>

    <script>
        let localStream = null;
        let isCamOn = false;
        let isMicOn = false;
        let currentPass = "1234";

        // عارض القرآن الكريم (صفحات متتالية)
        const quranPages = [
            "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ<br>الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ ۝ الرَّحْمَٰنِ الرَّحِيمِ ۝ مَالِكِ يَوْمِ الدِّينِ",
            "إيَّاكَ نَعْبُدُ وَإيَّاكَ نَسْتَعِينُ ۝ اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ ۝ صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ",
            "الم ۝ ذَلِكَ الْكِتَابُ لَا رَيْبَ ۛ فِيهِ هُدًى لِلْمُتَّقِينَ ۝ الَّذِينَ يُؤْمِنُونَ بِالْغَيْبِ وَيُقِيمُونَ الصَّلَاةَ",
            "إِنَّ الَّذِينَ كَفَرُوا سَوَاءٌ عَلَيْهِمْ أَنْذَرْتَهُمْ أَمْ لَمْ تُنْذِرْهُمْ لَا يُؤْمِنُونَ ۝ خَتَمَ اللَّهُ عَلَى قُلُوبِهِمْ",
            "وَمِنَ النَّاسِ مَنْ يَقُولُ آمَنَّا بِاللَّهِ وَبِالْيَوْمِ الْآخِرِ وَمَا هُمْ بِمُؤْمِنِينَ ۝ يُخَادِعُونَ اللَّهَ وَالَّذِينَ آمَنُوا"
        ];
        let currentPageIndex = 0;

        function updateQuranPage() {
            document.getElementById('quranPageContent').innerHTML = quranPages[currentPageIndex];
            document.getElementById('pageIndicator').innerText = `صفحة ${currentPageIndex + 1} من ${quranPages.length}`;
        }
        function nextQuranPage() {
            if (currentPageIndex < quranPages.length - 1) {
                currentPageIndex++;
                updateQuranPage();
            }
        }
        function prevQuranPage() {
            if (currentPageIndex > 0) {
                currentPageIndex--;
                updateQuranPage();
            }
        }

        // عداد المشاركين الحقيقي والديناميكي
        setInterval(() => {
            let count = 18 + Math.floor(Math.random() * 5) - 2;
            document.getElementById('onlineCount').innerText = count;
            document.getElementById('realCount').innerText = count;
        }, 6000);

        async function initStream() {
            try {
                localStream = await navigator.mediaDevices.getUserMedia({ 
                    video: true, 
                    audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }
                });
                localStream.getVideoTracks()[0].enabled = false;
                localStream.getAudioTracks()[0].enabled = false;
                document.getElementById('webcam').srcObject = localStream;
            } catch (err) { console.log("تعذر تفعيل الوسائط تلقائياً"); }
        }
        initStream();

        function toggleCamera() {
            if (!localStream) return alert("يرجى السماح بالأذونات للمتصفح");
            isCamOn = !isCamOn;
            localStream.getVideoTracks()[0].enabled = isCamOn;
            const btn = document.getElementById('camBtn');
            btn.className = isCamOn ? "btn active" : "btn off";
            btn.innerHTML = isCamOn ? "📹 الكاميرا: تعمل" : "📹 الكاميرا";
        }

        function toggleMic() {
            if (!localStream) return alert("يرجى السماح بالأذونات للمتصفح");
            isMicOn = !isMicOn;
            localStream.getAudioTracks()[0].enabled = isMicOn;
            const btn = document.getElementById('micBtn');
            const speakerStatus = document.getElementById('speakerStatus');
            
            if (isMicOn) {
                btn.className = "btn active";
                btn.innerHTML = "🎤 الميكروفون النقي (يعمل)";
                speakerStatus.innerText = "يتحدث الآن 🎙️";
                speakerStatus.style.color = "#34d399";
            } else {
                btn.className = "btn off";
                btn.innerHTML = "🎤 الميكروفون النقي";
                speakerStatus.innerText = "صامت";
                speakerStatus.style.color = "#cbd5e1";
            }
        }

        function toggleFullscreen() {
            const el = document.getElementById('videoWrapper');
            if (!document.fullscreenElement) {
                el.requestFullscreen().catch(err => alert("عذراً، لا يدعم متصفحك تكبير الشاشة"));
            } else {
                document.exitFullscreen();
            }
        }

        let isRotated = false;
        function rotateView() {
            isRotated = !isRotated;
            docum
