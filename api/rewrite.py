import os
from flask import jsonify, request
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def handler(request):
    try:
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

        prompt = (
            f"Rewrite the following email in a {tone_desc} tone. "
            "Keep the meaning identical, improve clarity, correct grammar, "
            "and keep it appropriate for professional email.\n\n"
            f"EMAIL:\n{email_text}\n\n"
            "Provide only the rewritten email (no commentary)."
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        rewritten_email = response.text.strip() if response.text else "No response"
        return jsonify({"rewritten_email": rewritten_email})
    except Exception as e:
        return jsonify({"error": str(e)}), 500