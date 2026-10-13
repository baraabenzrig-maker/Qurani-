from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qurani - غرفة البث التفاعلية الممتورة</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #090d16, #111827, #1e1b4b);
            color: #ffffff;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        header {
            background: rgba(15, 23, 42, 0.9);
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
            padding: 6px 15px;
            border-radius: 12px;
            font-size: 13px;
            border: 1px solid rgba(56, 189, 248, 0.2);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 350px;
        }
        .online-badge {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 13px;
            border: 1px solid rgba(52, 211, 153, 0.3);
        }
        .main-container {
            display: flex;
            flex: 1;
            height: calc(100vh - 55px);
            overflow: hidden;
        }
        .stream-section {
            flex: 3;
            display: flex;
            flex-direction: column;
            padding: 15px;
            gap: 12px;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .video-box {
            position: relative;
            width: 100%;
            max-width: 680px;
            height: 380px;
            background: #000;
            border-radius: 16px;
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
            gap: 12px;
            background: rgba(30, 41, 59, 0.85);
            padding: 10px 18px;
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
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: 0.2s;
        }
        .btn:hover {
            background: #475569;
        }
        .btn.active {
            background: #0284c7;
        }
        .btn.off {
            background: #ef4444;
        }
        .zoom-controls {
            display: flex;
            gap: 6px;
            align-items: center;
        }
        .zoom-btn {
            background: #1e293b;
            color: #38bdf8;
            border: 1px solid #38bdf8;
            padding: 7px 10px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 12px;
        }
        .zoom-btn:hover {
            background: #0284c7;
            color: white;
        }
        .audio-player-bar {
            background: rgba(30, 41, 59, 0.7);
            padding: 6px 15px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .audio-player-bar button {
            background: #10b981;
            border: none;
            color: white;
            padding: 4px 10px;
            border-radius: 8px;
            cursor: pointer;
        }
        .chat-sidebar {
            flex: 1;
            max-width: 300px;
            background: rgba(15, 23, 42, 0.92);
            border-left: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            padding: 12px 15px;
            font-weight: bold;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: #38bdf8;
            background: rgba(30, 41, 59, 0.5);
            font-size: 14px;
        }
        .chat-messages {
            flex: 1;
            padding: 12px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .message {
            background: #1e293b;
            padding: 8px 12px;
            border-radius: 10px;
            max-width: 85%;
            font-size: 13px;
            line-height: 1.4;
        }
        .message.incoming {
            align-self: flex-start;
            border-bottom-right-radius: 2px;
        }
        .message.outgoing {
            align-self: flex-end;
            background: #0284c7;
            border-bottom-left-radius: 2px;
        }
        .chat-input-area {
            padding: 10px;
            display: flex;
            gap: 6px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(15, 23, 42, 0.95);
        }
        .chat-input-area input {
            flex: 1;
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px 12px;
            border-radius: 18px;
            color: white;
            outline: none;
            font-size: 13px;
        }
        .chat-input-area button {
            background: #0284c7;
            color: white;
            border: none;
            padding: 0 14px;
            border-radius: 18px;
            cursor: pointer;
            font-size: 13px;
        }
        @media(max-width: 768px) {
            .main-container {
                flex-direction: column;
            }
            .chat-sidebar {
                max-width: 100%;
                height: 140px;
            }
            .video-box {
                height: 210px;
            }
            .quran-ticker {
                display: none;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">📖 Qurani Live</div>
        <div class="quran-ticker" id="tickerText">✨ "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي" ✨</div>
        <div class="online-badge">🟢 المتواجدون: <strong>27 مستخدماً</strong></div>
    </header>

    <div class="main-container">
        <div class="stream-section">
            <div class="video-box">
                <video id="webcam" autoplay playsinline></video>
            </div>
            
            <!-- مشغل تلاوة قرآنية هادئة -->
            <div class="audio-player-bar">
                <span>🎧 تلاوة خاشعة في الخلفية:</span>
                <button id="audioBtn" onclick="toggleAudio()">تشغيل التلاوة</button>
                <audio id="bgAudio" loop src="https://server11.mp3quran.net/sds/001.mp3"></audio>
            </div>

            <!-- أزرار التحكم -->
            <div class="controls">
                <button id="camBtn" class="btn off" onclick="toggleCamera()">📹 الكاميرا: معطلة</button>
                <button id="micBtn" class="btn off" onclick="toggleMic()">🎤 الميكروفون: معطل</button>
                <div class="zoom-controls">
                    <button class="zoom-btn" onclick="zoomIn()">➕ تكبير</button>
                    <button class="zoom-btn" onclick="zoomOut()">➖ تصغير</button>
                </div>
            </div>
        </div>

        <div class="chat-sidebar">
            <div class="chat-header">دردشة الغرفة التفاعلية</div>
            <div class="chat-messages" id="chatBox">
                <div class="message incoming"><strong>محمد:</strong> تقبل الله طاعتكم أجمعين</div>
                <div class="message incoming"><strong>سارة:</strong> ما أجمل هذه الأجواء المباركة</div>
                <div class="message outgoing"><strong>أنت:</strong> أهلاً بالجميع، نورتنا الغرفة</div>
            </div>
            <div class="chat-input-area">
                <input type="text5" id="msgInput" placeholder="اكتب رسالة..." onkeypress="handleKey(event)">
                <button onclick="sendMessage()">إرسال</button>
            </div>
        </div>
    </div>

    <script>
        let localStream = null;
        let isCamOn = false;
        let isMicOn = false;
        let currentZoom = 1;

        async function initStream() {
            try {
                localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                localStream.getVideoTracks()[0].enabled = false;
                localStream.getAudioTracks()[0].enabled = false;
                document.getElementById('webcam').srcObject = localStream;
            } catch (err) {
                console.log("تعذر الحصول على الوسائط تلقائياً: ", err);
            }
        }
        initStream();

        function toggleCamera() {
            if (!localStream) {
                alert("يرجى السماح بالوصول للأذونات من المتصفح");
                return;
            }
            const videoTrack = localStream.getVideoTracks()[0];
            isCamOn = !isCamOn;
            videoTrack.enabled = isCamOn;
            
            const btn = document.getElementById('camBtn');
            if (isCamOn) {
                btn.className = "btn active";
                btn.innerHTML = "📹 الكاميرا: تعمل";
            } else {
                btn.className = "btn off";
                btn.innerHTML = "📹 الكاميرا: معطلة";
            }
        }

        function toggleMic() {
            if (!localStream) {
                alert("يرجى السماح بالوصول للأذونات من المتصفح");
                return;
            }
            const audioTrack = localStream.getAudioTracks()[0];
            isMicOn = !isMicOn;
            audioTrack.enabled = isMicOn;
            
            const btn = document.getElementById('micBtn');
            if (isMicOn) {
                btn.className = "btn active";
                btn.innerHTML = "🎤 الميكروفون: يعمل";
            } else {
                btn.className = "btn off";
                btn.innerHTML = "🎤 الميكروفون: معطل";
            }
        }

        function zoomIn() {
            if (currentZoom < 2.5) {
                currentZoom += 0.25;
                document.getElementById('webcam').style.transform = `scale(${currentZoom})`;
            }
        }

        function zoomOut() {
            if (currentZoom > 1) {
                currentZoom -= 0.25;
                document.getElementById('webcam').style.transform = `scale(${currentZoom})`;
            }
        }

        let isAudioPlaying = false;
        function toggleAudio() {
            const audio = document.getElementById('bgAudio');
            const btn = document.getElementById('audioBtn');
            if (!isAudioPlaying) {
                audio.play();
                btn.innerText = "إيقاف التلاوة";
                btn.style.background = "#ef4444";
                isAudioPlaying = true;
            } else {
                audio.pause();
                btn.innerText = "تشغيل التلاوة";
                btn.style.background = "#10b981";
                isAudioPlaying = false;
            }
        }

        function sendMessage() {
            const input = document.getElementById('msgInput');
            const text = input.value.trim();
            if (text === "") return;

            const chatBox = document.getElementById('chatBox');
            const msgDiv = document.createElement('div');
            msgDiv.className = "message outgoing";
            msgDiv.innerHTML = `<strong>أنت:</strong> ${text}`;
            chatBox.appendChild(msgDiv);
            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKey(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        }

        // تغيير الآيات في الأعلى تلقائياً كل 10 ثوانٍ
        const ayat = [
            '✨ "رَبِّ اشْرَحْ لِي صَدْرِي وَيَسِّرْ لِي أَمْرِي" ✨',
            '📖 "وَإِذَا قُرِئَ الْقُرْآنُ فَاستَمِعُوا لَهُ وَأَنصِتُوا" 📖',
            '💚 "أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ" 💚',
            '🌟 "وَقُل رَّبِّ زِدْنِي عِلْماً" 🌟'
        ];
        let ayatIndex = 0;
        setInterval(() => {
            ayatIndex = (ayatIndex + 1) % ayat.length;
            document.getElementById('tickerText').innerText = ayat;
        }, 10000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
