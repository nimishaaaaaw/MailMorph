import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/rewrite", methods=["POST"])
def rewrite_email():
    data = request.get_json()
    email_text = data.get("email", "").strip()
    tone = data.get("tone", "formal").strip().lower()

    if not email_text:
        return jsonify({"error": "Email text is empty"}), 400

    tone_map = {
        "formal": "formal and professional",
        "polite": "polite and friendly",
        "concise": "short and clear"
    }
    tone_desc = tone_map.get(tone, "formal and professional")

    # ✅ Strict prompt to avoid explanations or extra text
    prompt = f"""
    You are an email rewriting assistant.
    Rewrite the following email in a {tone_desc} tone.
    Keep the meaning the same, improve grammar and clarity, 
    and make it sound professional and natural.
    ❌ Do NOT include explanations, options, or titles.
    ✅ Only return the rewritten email text — no extra output.

    EMAIL:
    {email_text}
    """

    try:
        # Use Gemini model
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)

        rewritten_email = response.text.strip() if response and response.text else "No output from model."
        return jsonify({"rewritten_email": rewritten_email})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)