from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, template_folder="../templates")

API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1-distill-llama-70b:free"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

# For static files (css, js, etc.) if needed
@app.route('/templates/<path:filename>')
def serve_static(filename):
    return send_from_directory('../templates', filename)

# For Vercel Python serverless
app = app 