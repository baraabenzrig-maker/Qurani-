from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qurani - البث المباشر</title>
    <style>
        body {
            font-family: Arial, sans-serif;
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
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #1e293b;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        video {
            width: 100%;
            height: auto;
            border-radius: 8px;
            background: #000;
            margin-top: 15px;
        }
        button {
            background-color: #0284c7;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 15px;
        }
        button:hover {
            background-color: #0369a1;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>مشروع Qurani المباشر</h1>
        <p>تشغيل الكاميرا والبث عبر الويب</p>
        <button onclick="startCamera()">تشغيل الكاميرا</button>
        <br>
        <video id="webcam" autoplay playsinline></video>
    </div>

    <script>
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                const videoElement = document.getElementById('webcam');
                videoElement.srcObject = stream;
            } catch (error) {
                alert("تعذر الوصول إلى الكاميرا: " + error.message);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
