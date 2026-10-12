from flask import Flask, render_template_string

app = Flask(__name__)

# قالب HTML بسيط وسريع يحتوي على مشغل الكاميرا والبث المباشر
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qurani - البث المباشر</title>
    <style>
        body {
            font-family: Tahoma, sans-serif;
            background-color: #0f172a;
            color: #ffffff;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #38bdf8;
            margin-bottom: 10px;
        }
        .video-container {
            margin: 20px auto;
            max-width: 600px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            background: #1e293b;
        }
        video {
            width: 100%;
            height: auto;
            display: block;
        }
        .btn {
            background-color: #0ea5e9;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
            transition: background 0.3s;
        }
        .btn:hover {
            background-color: #0284c7;
        }
    </style>
</head>
<body>

    <h1>موقع Qurani للبث المباشر</h1>
    <p>أهلاً بك! افتح الكاميرا للبدء بالبث والتلاوة.</p>

    <div class="video-container">
        <video id="webcam" autoplay playsinline></video>
    </div>

    <button class="btn" id="start-btn">تشغيل الكاميرا</button>

    <script>
        const startBtn = document.getElementById('start-btn');
        const webcamElement = document.getElementById('webcam');

        startBtn.addEventListener('click', async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                webcamElement.srcObject = stream;
                startBtn.style.display = 'none';
            } catch (err) {
                alert('تعذر الوصول إلى الكاميرا أو الميكروفون. تأكد من منح الصلاحيات.');
                console.error(err);
            }
        });
    </script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)# Qurani-
live Quran streaming 
