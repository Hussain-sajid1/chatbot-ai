from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, template_folder="../templates")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {"parts": [{"text": user_message}]}
        ]
    }
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        data = response.json()
        print("GEMINI RAW RESPONSE:", data)
        if "candidates" in data and data["candidates"]:
            bot_reply = data["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in data:
            bot_reply = f"Gemini API error: {data['error'].get('message', str(data['error']))}"
        else:
            bot_reply = f"Unexpected Gemini response: {data}"
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

@app.route('/templates/<path:filename>')
def serve_static(filename):
    return send_from_directory('../templates', filename)

# For Vercel Python serverless
app = app 