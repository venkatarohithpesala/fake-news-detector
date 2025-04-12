from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')

    prompt = f"""
You are a fake news checker assistant. A user will input a question, rumor, or headline.
Your task is to say whether it's likely to be true or false and explain briefly (2–3 sentences max).

Input:
{text}

Respond in plain English.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or use "gpt-4" if preferred
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response['choices'][0]['message']['content']
        return jsonify({ "explanation": content })

    except Exception as e:
        print("Error:", e)
        return jsonify({ "error": "OpenAI API request failed." }), 500

if __name__ == '__main__':
    app.run(debug=True)
