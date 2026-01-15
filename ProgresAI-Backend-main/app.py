from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
ASSISTANT_NAME = "ProgresAI"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        user_name = data.get("user_name")

        print(f"Received message: {user_message} from {user_name}")  # Debugging

        system_message = f"""
        Hello, I am {user_name}, You are {ASSISTANT_NAME}, a career guidance chatbot. 
        *** Reply in concise, helpful responses and in English only. ***
        """

        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 1
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        print("Groq API Response:", response.text)  # Debugging

        if response.status_code == 200:
            response_data = response.json()
            assistant_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "I'm not sure how to respond.")
            return jsonify({"assistant_message": assistant_message}), 200
        else:
            return jsonify({"error": f"API error: {response.status_code}, {response.text}"}), 500

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
