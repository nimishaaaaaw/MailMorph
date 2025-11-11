import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS
import google.generativeai as genai  # ✅ Correct import for Gemini SDK

# ----------------------------
# Environment and API Key Setup
# ----------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment")

# ✅ Configure the Gemini SDK with your API key
genai.configure(api_key=GOOGLE_API_KEY)

# ----------------------------
# Flask App Initialization
# ----------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rewrite", methods=["POST"])
def rewrite_email():
    """Rewrites an email using Google Gemini"""
    data = request.get_json(force=True)
    email_text = data.get("email", "").strip()
    tone = data.get("tone", "formal").strip().lower()

    if not email_text:
        return jsonify({"error": "Empty email text"}), 400

    tone_map = {
        "formal": "formal and professional",
        "polite": "polite and friendly",
        "concise": "short and concise"
    }
    tone_desc = tone_map.get(tone, "formal and professional")

    # The prompt that Gemini will use
    prompt = (
        f"Rewrite the following email in a {tone_desc} tone. "
        "Keep the meaning identical, improve clarity, correct grammar, "
        "and ensure it sounds polite and natural.\n\n"
        f"EMAIL:\n{email_text}\n\n"
        "Return only the rewritten email text, with no extra comments."
    )

    try:
        # ✅ Use the official Gemini SDK
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)

        # Extract text safely
        rewritten_email = response.text.strip() if response.text else "No response from model."

        return jsonify({"rewritten_email": rewritten_email})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------------------------
# Main entry point
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)