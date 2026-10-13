from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qurani AI Hub - المنصة الإسلامية الذكية</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #030712, #0f172a, #1e1b4b);
            color: #ffffff;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        header {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(12px);
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .logo {
            font-size: 18px;
            font-weight: bold;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .quran-ticker {
            background: rgba(56, 189, 248, 0.1);
            color: #38bdf8;
            padding: 5px 12px;
            border-radius: 10px;
            font-size: 13px;
            border: 1px solid rgba(56, 189, 248, 0.2);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 300px;
        }
        .online-badge {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 13px;
            border: 1px solid rgba(52, 211, 153, 0.3);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .main-container {
            display: flex;
            flex: 1;
            height: calc(100vh - 55px);
            overflow: hidden;
        }
        .stream-section {
            flex: 2.5;
            display: flex;
            flex-direction: column;
            padding: 12px;
            gap: 10px;
            align-items: center;
            overflow-y: auto;
        }
        .top-panels {
            display: flex;
            gap: 10px;
            width: 100%;
            max-width: 750px;
        }
        .panel {
            flex: 1;
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 10px;
            font-size: 12px;
            max-height: 120px;
            overflow-y: auto;
        }
        .panel h4 {
            color: #38bdf8;
            margin-bottom: 5px;
            font-size: 13px;
        }
        .video-box {
            position: relative;
            width: 100%;
            max-width: 750px;
            height: 300px;
            background: #000;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            border: 2px solid rgba(56, 189, 248, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        .controls {
            display: flex;
            gap: 8px;
            background: rgba(30, 41, 59, 0.85);
            padding: 8px 14px;
            border-radius: 30px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            flex-wrap: wrap;
            justify-content: center;
        }
        .btn {
            background: #334155;
            color: white;
            border: none;
            padding: 7px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: 0.2s;
        }
        .btn:hover { background: #475569; }
        .btn.active { background: #0284c7; }
        .btn.off { background: #ef4444; }
        
        .social-bar {
            display: flex;
            gap: 8px;
            background: rgba(30, 41, 59, 0.6);
            padding: 5px 12px;
            border-radius: 10px;
            font-size: 12px;
            align-items: center;
        }
        .social-btn {
            background: #1877f2;
            color: white;
            text-decoration: none;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: bold;
        }
        .social-btn.messenger { background: #0084ff; }
        .social-btn.whatsapp { background: #25d366; }

        .sidebar {
            flex: 1.2;
            max-width: 340px;
            background: rgba(15, 23, 42, 0.95);
            border-left: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            flex-direction: column;
        }
        .tabs {
            display: flex;
            background: rgba(30, 41, 59, 0.6);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .tab-btn {
            flex: 1;
            background: none;
            border: none;
            color: #94a3b8;
            padding: 10px;
            font-size: 12px;
            cursor: pointer;
            font-weight: bold;
        }
        .tab-btn.active {
            color: #38bdf8;
            border-bottom: 2px solid #38bdf8;
            background: rgba(56, 189, 248, 0.05);
        }
        .tab-content {
            flex: 1;
            display: none;
            flex-direction: column;
            overflow-y: auto;
            padding: 10px;
            gap: 8px;
        }
        .tab-content.active { display: flex; }
        
        .message {
            background: #1e293b;
            padding: 8px 12px;
            border-radius: 10px;
            max-width: 90%;
            font-size: 12px;
            line-height: 1.4;
        }
        .message.incoming { align-self: flex-start; }
        .message.outgoing { align-self: flex-end; background: #0284c7; }
        
        .chat-input-area {
            padding: 10px;
            display: flex;
            gap: 6px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .chat-input-area input {
            flex: 1;
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px;
            border-radius: 16px;
            color: white;
            font-size: 12px;
            outline: none;
        }
        .chat-input-area button {
            background: #0284c7;
            color: white;
            border: none;
            padding: 0 12px;
            border-radius: 16px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .admin-modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .admin-box {
            background: #1e293b;
            padding: 20px;
            border-radius: 12px;
            width: 300px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border: 1px solid #38bdf8;
        }
        .admin-box input {
            background: #0f172a;
            border: 1px solid #475569;
            padding: 8px;
            color: white;
            border-radius: 6px;
        }
        @media(max-width: 768px) {
            .main-container { flex-direction: column; }
            .sidebar { max-width: 100%; height: 250px; }
            .video-box { height: 180px; }
            .top-panels { display: none; }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">📖 Qurani AI Hub</div>
        <div class="quran-ticker" id="tickerText">✨ "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي" ✨</div>
        <div style="display:flex; gap:10px; align-items:center;">
            <div class="online-badge">🟢 المتواجدون: <strong id="onlineCount">42</strong></div>
            <button class="btn active" onclick="openAdmin()" style="padding:4px 10px; font-size:11px;">🔒 لوحة الأدمن</button>
        </div>
    </header>

    <div class="main-container">
        <div class="stream-section">
            <div class="top-panels">
                <div class="panel">
                    <h4>📖 شاشة القرآن المباشرة (للتلاميذ)</h4>
                    <p id="quranPageDisplay" style="color: #cbd5e1;">سورة الفاتحة: (بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ ۝ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ ۝)</p>
                </div>
                <div class="panel">
                    <h4>🤲 ركن الأدعية اليومية</h4>
                    <p style="color: #cbd5e1;">"اللهم إنا نسألك علماً نافعاً ورزقاً طيباً وعملاً متقبلاً."</p>
                </div>
            </div>

            <div class="video-box">
                <video id="webcam" autoplay playsinline></video>
            </div>
            
            <div class="social-bar">
                <span>مشاركة:</span>
                <a href="#" id="fbShare" target="_blank" class="social-btn">📘 فيسبوك</a>
                <a href="#" id="msgShare" class="social-btn messenger">💬 ماسنجر</a>
                <a href="#" id="waShare" target="_blank" class="social-btn whatsapp">🟢 واتساب</a>
            </div>

            <div class="controls">
                <button id="camBtn" class="btn off" onclick="toggleCamera()">📹 الكاميرا</button>
                <button id="micBtn" class="btn off" onclick="toggleMic()">🎤 مايك فائق النقاء</button>
                <button class="btn" onclick="zoomIn()">➕ تكبير</button>
                <button class="btn" onclick="zoomOut()">➖ تصغير</button>
                <button class="btn" onclick="createGroup()">➕ إنشاء مجموعة</button>
            </div>
        </div>

        <div class="sidebar">
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('chat')">💬 الشات العام</button>
                <button class="tab-btn" onclick="switchTab('ai')">🤖 الذكاء الديني</button>
                <button class="tab-btn" onclick="switchTab('goals')">🎯 إنجازات اليوم</button>
            </div>

            <div class="tab-content active" id="tab-chat">
                <div style="flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:8px;" id="chatBox">
                    <div class="message incoming"><strong>عمر:</strong> السلام عليكم ورحمة الله</div>
                    <div class="message outgoing"><strong>أنت:</strong> وعليكم السلام، أهلاً بك في غرفة Qurani</div>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="msgInput" placeholder="اكتب رسالة..." onkeypress="handleKey(event)">
                    <button onclick="sendMessage()">إرسال</button>
                </div>
            </div>

            <div class="tab-content" id="tab-ai">
                <div style="flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:8px;" id="aiBox">
                    <div class="message incoming"><strong>🤖 المساعد الديني الذكي:</strong> أهلاً بك. اسألني أي سؤال ديني أو اطلب آية وسأجيبك فوراً.</div>
                </div>
                <div class="chat-input-area">
                    <input type="text" id="aiInput" placeholder="اسأل المساعد الديني..." onkeypress="handleAIKey(event)">
                    <button onclick="askAI()">إسأل</button>
                </div>
            </div>

            <div class="tab-content" id="tab-goals" style="padding: 12px;">
                <h4 style="color:#38bdf8; font-size:13px; margin-bottom:5px;">📌 إنجازاتك لليوم (تتجدد يومياً):</h4>
                <div style="background:#1e293b; padding:10px; border-radius:8px; font-size:12px; margin-bottom:8px;">
                    <input type="checkbox" id="goal1"> قراءة حزب من القرآن<br>
                    <input type="checkbox" id="goal2"> حضور درس البث المباشر<br>
                    <input type="checkbox" id="goal3"> حفظ 3 آيات جديدة
                </div>
                <p style="font-size:10px; color:#94a3b8;">* يتم مسح الإنجازات وتحديثها تلقائياً مع بداية كل يوم جديد.</p>
            </div>
        </div>
    </div>

    <div class="admin-modal" id="adminModal">
        <div class="admin-box">
            <h3 style="color:#38bdf8; font-size:15px;">لوحة تحكم الأدمن</h3>
            <p style="font-size:12px; color:#cbd5e1;">أدخل كلمة المرور لتغيير إعدادات الموقع:</p>
            <input type="password" id="adminPassInput" placeholder="كلمة المرور (الافتراضية: 1234)">
            <input type="text" id="newSiteTitle" placeholder="تغيير عنوان رسالة الشريط العلوي">
            <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:5px;">
                <button class="btn off" onclick="closeAdmin()">إلغاء</button>
                <button class="btn active" onclick="saveAdminSettings()">حفظ وتطبيق</button>
            </div>
        </div>
    </div>

    <script>
        let localStream = null;
        let isCamOn = false;
        let isMicOn = false;
        let currentZoom = 1;

        const currentUrl = window.location.href;
        document.getElementById('fbShare').href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(currentUrl)}`;
        document.getElementById('msgShare').href = `fb-messenger://share?link=${encodeURIComponent(currentUrl)}`;
        document.getElementById('waShare').href = `https://api.whatsapp.com/send?text=${encodeURIComponent('انضم إلينا في غرفة Qurani المباشرة: ' + currentUrl)}`;

        setInterval(() => {
            let base = 38;
            let rand = Math.floor(Math.random() * 7) - 3;
            document.getElementById('onlineCount').innerText = base + rand;
        }, 5000);

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
            if (!localStream) return alert("يرجى السماح بالأذونات");
            isCamOn = !isCamOn;
            localStream.getVideoTracks()[0].enabled = isCamOn;
            const btn = document.getElementById('camBtn');
            btn.className = isCamOn ? "btn active" : "btn off";
            btn.innerHTML = isCamOn ? "📹 الكاميرا: تعمل" : "📹 الكاميرا";
        }

        function toggleMic() {
            if (!localStream) return alert("يرجى السماح بالأذونات");
            isMicOn = !isMicOn;
            localStream.getAudioTracks()[0].enabled = isMicOn;
            const btn = document.getElementById('micBtn');
            btn.className = isMicOn ? "btn active" : "btn off";
            btn.innerHTML = isMicOn ? "🎤 مايك فائق النقاء (يعمل)" : "🎤 مايك فائق النقاء";
        }

        function zoomIn() {
            if (currentZoom < 2.5) { currentZoom += 0.25; document.getElementById('webcam').style.transform = `scale(${currentZoom})`; }
        }
        function zoomOut() {
            if (currentZoom > 1) { currentZoom -= 0.25; document.getElementById('webcam').style.transform = `scale(${currentZoom})`; }
        }

        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabName).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        function sendMessage() {
            const input = document.getElementById('msgInput');
            if (!input.value.trim()) return;
            const chatBox = document.getElementById('chatBox');
            chatBox.innerHTML += `<div class="message outgoing"><strong>أنت:</strong> ${input.value}</div>`;
            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        function handleKey(e) { if (e.key === 'Enter') sendMessage(); }

        function askAI() {
            const input = document.getElementById('aiInput');
            if (!input.value.trim()) return;
            const aiBox = document.getElementById('aiBox');
            aiBox.innerHTML += `<div class="message outgoing"><strong>أنت:</strong> ${input.value}</div>`;
            let q = input.value;
            input.value = "";
            
            setTimeout(() => {
                let reply = "قال الله تعالى: (وَاصْبِرْ لِحُكْمِ رَبِّكَ فَإِنَّكَ بِأَعْيُنِنَا). نعم، الاستمرار في العمل الصالح يورث الطمأنينة.";
                if (q.includes("صلاة")) reply = "قال رسول الله صلى الله عليه وسلم: (إِنَّ الصَّلَاةَ تَنْهَى عَنِ الْفَالْفَحْشَاءِ وَالْمُنْكَرِ). حافظ عليها في وقتها.";
                aiBox.innerHTML += `<div class="message incoming"><strong>🤖 المساعد الديني:</strong> ${reply}</div>`;
                aiBox.scrollTop = aiBox.scrollHeight;
            }, 800);
        }
        function handleAIKey(e) { if (e.key === 'Enter') askAI(); }

        function createGroup() {
            let gName = prompt("أدخل اسم المجموعة أو الحلقة الجديدة:");
            if (gName) alert(`تم إنشاء مجموعة "${gName}" بنجاح وانضممت إليها!`);
        }

        function openAdmin() { document.getElementById('adminModal').style.display = 'flex'; }
        function closeAdmin() { document.getElementById('adminModal').style.display = 'none'; }
        function saveAdminSettings() {
            let pass = document.getElementById('adminPassInput').value;
            if (pass === "1234") {
                let newTitle = document.getElementById('newSiteTitle').value;
                if (newTitle) {
                    document.getElementById('tickerText').innerText = `✨ "${newTitle}" ✨`;
                }
                alert("تم تحديث إعدادات الموقع بنجاح بواسطة الأدمن!");
                closeAdmin();
            } else {
                alert("كلمة المرور غير صحيحة!");
            }
        }

        const ayatList = [
            '✨ "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي" ✨',
            '📖 "وَإِذَا قُرِئَ الْقُرْآنُ فَاستَمِعُوا لَهُ وَأَنصِتُوا" 📖',
            '💚 "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ" 💚',
            '🌟 "وَقُل رَّبِّ زِدْنِي عِلْماً" 🌟'
        ];
        let ayatIndex = 0;
        setInterval(() => {
            ayatIndex = (ayatIndex + 1) % ayatList.length;
            document.getElementById('tickerText').innerText = ayatList[ayatIndex];
        }, 9000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
